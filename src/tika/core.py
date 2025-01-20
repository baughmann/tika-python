#!/usr/bin/env python
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Module documentation
"""
Tika Python module provides Python API client to Apache Tika Server.

**Example usage**::

    import tika
    from tika import parser
    parsed = parser.from_file('/path/to/file')
    print(parsed["metadata"])
    print(parsed["content"])

Visit https://github.com/chrismattmann/tika-python to learn more about it.

**Detect IANA MIME Type**::

    from tika import detector
    print(detector.from_file('/path/to/file'))

**Detect Language**::

    from tika import language
    print(language.from_file('/path/to/file'))

***Tika-Python Configuration***
You can now use custom configuration files. See https://tika.apache.org/1.18/configuring.html
for details on writing configuration files. Configuration is set the first time the server is started.
To use a configuration file with a parser, or detector:
    parsed = parser.from_file('/path/to/file', config_path='/path/to/configfile')
or:
    detected = detector.from_file('/path/to/file', config_path='/path/to/configfile')
or:
    detected = detector.from_buffer('some buffered content', config_path='/path/to/configfile')

"""

import codecs
import getopt
import hashlib
import logging
import os
import platform
import re
import signal
import socket
import sys
import tempfile
import time
import types
from collections.abc import Iterable
from http import HTTPStatus
from os import walk
from pathlib import Path
from subprocess import STDOUT, Popen
from typing import Any, BinaryIO, Literal, NoReturn, TypedDict

import requests

USAGE = """
tika.py [-v] [-e] [-o <outputDir>] [--server <Tikaserver_endpoint>] [--install <UrlToTikaServerJar>] [--port <portNumber>] <command> <option> <urlOrPathToFile>

tika.py parse all test.pdf test2.pdf                   (write output JSON metadata files for test1.pdf_meta.json and test2.pdf_meta.json)
tika.py detect type test.pdf                           (returns mime-type as text/plain)
tika.py language file french.txt                       (returns language e.g., fr as text/plain)
tika.py translate fr:en french.txt                     (translates the file french.txt from french to english)
tika.py config mime-types                              (see what mime-types the Tika Server can handle)

A simple python and command-line client for Tika using the standalone Tika server (JAR file).
All commands return results in JSON format by default (except text in text/plain).

To parse docs, use:
tika.py parse <meta | text | all> <path>

To check the configuration of the Tika server, use:
tika.py config <mime-types | detectors | parsers>

Commands:
  parse  = parse the input file and write a JSON doc file.ext_meta.json containing the extracted metadata, text, or both
  detect type = parse the stream and 'detect' the MIME/media type, return in text/plain
  language file = parse the file stream and identify the language of the text, return its 2 character code in text/plain
  translate src:dest = parse and extract text and then translate the text from source language to destination language
  config = return a JSON doc describing the configuration of the Tika server (i.e. mime-types it
             can handle, or installed detectors or parsers)

Arguments:
  urlOrPathToFile = file to be parsed, if URL it will first be retrieved and then passed to Tika

Switches:
  --verbose, -v                  = verbose mode
  --encode, -e           = encode response in UTF-8
  --csv, -c    = report detect output in comma-delimited format
  --server <Tikaserver_endpoint>  = use a remote Tika Server at this endpoint, otherwise use local server
  --install <UrlToTikaServerJar> = download and exec Tika Server (JAR file), starting server on default port 9998

Example usage as python client:
-- from tika import runCommand, parse1
-- jsonOutput = runCommand('parse', 'all', filename)
 or
-- jsonOutput = parse1('all', filename)

"""  # noqa: E501


class TikaResponse(TypedDict):
    status: int
    metadata: dict[str, str | list[str]] | None
    content: str | bytes | BinaryIO | None
    attachments: dict[str, Any] | None


try:
    unicode_string = unicode  # type: ignore
    binary_string = str
except NameError:
    unicode_string = str
    binary_string = bytes

try:
    from urllib import urlretrieve  # type: ignore
except ImportError:
    from urllib.request import urlretrieve
try:
    from urlparse import urlparse  # type: ignore
except ImportError:
    from urllib.parse import urlparse as urlparse

try:
    from rfc6266 import build_header  # type: ignore

    def make_content_disposition_header(fn: str | Path) -> Any:  # type: ignore # noqa: ANN201, ANN401
        return build_header(os.path.basename(fn)).decode("ascii")
except ImportError:

    def make_content_disposition_header(fn: str | Path) -> str:
        return f"attachment; filename={os.path.basename(fn)}"


LOG_DIR = Path(os.getenv("TIKA_LOG_PATH", tempfile.gettempdir()))
LOG_FILE = Path(os.path.join(LOG_DIR, os.getenv("TIKA_LOG_FILE", "tika.log")))

log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger: logging.Logger = logging.getLogger("tika.tika")

if os.getenv("TIKA_LOG_FILE", "tika.log"):
    print(f"Logging to {LOG_FILE}")  # noqa: T201
    # File logs
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    # Stdout logs
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

# Log level
logger.setLevel(logging.DEBUG)

IS_WINDOWS = platform.system() == "Windows"
TIKA_VERSION = os.getenv("TIKA_VERSION", "3.0.0")
TIKA_JAR_PATH = Path(os.getenv("TIKA_PATH", tempfile.gettempdir()))
TIKA_FILES_PATH = Path(tempfile.gettempdir())
TIKA_SERVER_LOG_FILE_PATH = LOG_DIR


def get_bundled_jar_path() -> Path:
    """Get path to bundled Tika server JAR file"""
    # python 3.9+
    try:
        from importlib.resources import files

        return Path(str(files("tika").joinpath("jars/tika-server-standard-3.0.0.jar")))
    # python 3.7-3.8
    except ImportError:
        from importlib.resources import path

        with path("tika", "jars/tika-server-standard-3.0.0.jar") as jar_path:
            return Path(str(jar_path))


# Replace the existing TikaServerJar definition
TIKA_SERVER_JAR = Path(os.getenv("TIKA_SERVER_JAR", get_bundled_jar_path()))
TIKA_JAR_HASH_ALGO: str = os.getenv("TIKA_JAR_HASH_ALGO", "md5")

SERVER_HOST = "localhost"
PORT = "9998"
SERVER_ENDPOINT: str = os.getenv("TIKA_SERVER_ENDPOINT", "http://" + SERVER_HOST + ":" + PORT)
TRANSLATOR: str = os.getenv("TIKA_TRANSLATOR", "org.apache.tika.language.translate.Lingo24Translator")
TIKA_CLIENT_ONLY = bool(os.getenv("TIKA_CLIENT_ONLY", default=False))
TIKA_SERVER_CLASSPATH: str = os.getenv("TIKA_SERVER_CLASSPATH", "")
TIKA_STARTUP_SLEEP = float(os.getenv("TIKA_STARTUP_SLEEP", 5))
TIKA_STARTUP_MAX_RETRY = int(os.getenv("TIKA_STARTUP_MAX_RETRY", 3))
TIKA_JAVA: str = os.getenv("TIKA_JAVA", "java")
TIKA_JAVA_ARGS: str = os.getenv("TIKA_JAVA_ARGS", "")

VERBOSE: int = 0
ENCODE_UTF8: int = 0
CSV_OUTPUT: int = 0

# will be used later on to kill the process and free up ram
TIKA_SERVER_PROCESS: Popen[bytes] | None = None


class TikaError(Exception):
    pass


def echo2(*s: Any) -> types.NoneType:  # noqa: ANN401
    sys.stderr.write(unicode_string("tika.py: %s\n") % unicode_string(" ").join(map(unicode_string, s)))


def warn(*s: Any) -> types.NoneType:  # noqa: ANN401
    echo2("Warn:", *s)


def die(*s: Any) -> NoReturn:  # noqa: ANN401
    warn("Error:", *s)
    echo2(USAGE)
    sys.exit()


def run_command(
    cmd: str,
    option: str,
    url_or_paths: Iterable[str | Path | BinaryIO],
    port: str,
    out_dir: Path | None = None,
    server_host: str = SERVER_HOST,
    tika_server_jar: Path = TIKA_SERVER_JAR,
    verbose: int = VERBOSE,
    encode: int = ENCODE_UTF8,
) -> list[Path] | list[tuple[int, str | bytes | BinaryIO]] | str | bytes | BinaryIO:
    """Execute a Tika command by calling the Tika server and return results.

    Args:
        cmd: The command to execute. Must be one of: 'parse', 'detect', 'language', 'translate', or 'config'.
        option: Command-specific option that modifies the behavior (e.g., 'all' for parse command).
        url_or_paths: One or more files to process, specified as URLs, file paths, or file-like objects.
        port: The port number where Tika server is running.
        out_dir: Optional directory path where output files should be saved. Defaults to None.
        server_host: The hostname where Tika server is running. Defaults to SERVER_HOST.
        tika_server_jar: Path to the Tika server JAR file. Defaults to TIKA_SERVER_JAR.
        verbose: Logging verbosity level. Defaults to VERBOSE.
        encode: Whether to encode response in UTF-8. Defaults to ENCODE_UTF8.

    Returns:
        Depending on the command:
            - For 'parse' with out_dir: List of Path objects for created metadata files
            - For 'parse' without out_dir: List of tuples containing (status_code, response)
            - For other commands: String, bytes or file-like object containing the response

    Raises:
        TikaError: If no URLs/paths are specified for parse/detect commands or if command is unknown.
    """
    if (cmd in "parse" or cmd in "detect") and not url_or_paths:
        msg = "No URLs/paths specified."
        logger.exception(msg)
        raise TikaError(msg)
    server_endpoint = "http://" + server_host + ":" + port
    if cmd == "parse":
        return parse_and_save(
            option=option,
            url_or_paths=url_or_paths,
            out_dir=out_dir,
            server_endpoint=server_endpoint,
            verbose=verbose,
            tika_server_jar=tika_server_jar,
        )
    if cmd == "detect":
        return detect_type(
            option=option,
            url_or_paths=url_or_paths,
            server_endpoint=server_endpoint,
            verbose=verbose,
            tika_server_jar=tika_server_jar,
        )
    if cmd == "language":
        return detect_lang(
            option=option,
            url_or_paths=url_or_paths,
            server_endpoint=server_endpoint,
            verbose=verbose,
            tika_server_jar=tika_server_jar,
        )
    if cmd == "config":
        status, resp = get_config(
            option=option,
            server_endpoint=server_endpoint,
            verbose=verbose,
            tika_server_jar=tika_server_jar,
        )
        if status != HTTPStatus.OK:
            msg = f"Unexpected response from Tika server ({status}): {resp}"
            raise TikaError(msg)
        return resp
    msg = f"Unknown command: {cmd}"
    logger.exception(msg)
    raise TikaError(msg)


def get_paths(url_or_paths: Iterable[str | Path | BinaryIO]) -> list[Path]:
    """Convert URLs, file paths, or file-like objects into a list of Path objects.

    Handles single paths, lists of paths, and directories. For directories,
    recursively finds all files within them.

    Args:
        url_or_paths: Input paths as URLs, file paths, directories, or file-like objects.
                     Can be a single item or an iterable of items.

    Returns:
        list[Path]: List of Path objects for all files found.

    Note:
        When a directory is provided, all files within it (including in subdirectories)
        are included in the returned list.
    """
    if not isinstance(url_or_paths, Iterable):
        url_or_paths = [url_or_paths]  # do not recursively walk over letters of a single path which can include "/"
    paths = []
    for each_url_or_paths in url_or_paths:
        if isinstance(each_url_or_paths, str | Path) and Path(each_url_or_paths).is_dir():
            for root, _, filenames in walk(each_url_or_paths):
                for filename in filenames:
                    paths.append(os.path.join(root, filename))
        else:
            paths.append(each_url_or_paths)
    return paths


def parse_and_save(
    option: str,
    url_or_paths: Iterable[str | Path | BinaryIO],
    *,
    out_dir: Path | None = None,
    server_endpoint: str = SERVER_ENDPOINT,
    verbose: int = VERBOSE,
    tika_server_jar: Path = TIKA_SERVER_JAR,
    response_mime_type: str = "application/json",
    meta_extension: str = "_meta.json",
    services: dict[str, str] | None = None,
) -> list[Path]:
    """Parse files and save extracted metadata/text as JSON files.

    For each input file, creates a corresponding metadata file with the specified extension.
    The metadata files contain the extracted information in JSON format.

    Args:
        option: Parsing option ('meta', 'text', or 'all').
        url_or_paths: Files to parse as URLs, paths, or file-like objects.
        out_dir: Directory where metadata files should be saved. If None,
                saves alongside input files. Defaults to None.
        server_endpoint: Tika server URL. Defaults to SERVER_ENDPOINT.
        verbose: Logging verbosity level. Defaults to VERBOSE.
        tika_server_jar: Path to Tika server JAR. Defaults to TIKA_SERVER_JAR.
        response_mime_type: Expected response format. Defaults to "application/json".
        meta_extension: Extension to append to metadata filenames. Defaults to "_meta.json".
        services: Dict mapping options to service endpoints. Defaults to
                 {'meta': '/meta', 'text': '/tika', 'all': '/rmeta'}.

    Returns:
        list[Path]: List of paths to the created metadata files.

    Note:
        For each input file 'example.pdf', creates 'example.pdf_meta.json'
        (or similar based on meta_extension) containing the extracted information.
    """
    services = services or {"meta": "/meta", "text": "/tika", "all": "/rmeta"}
    meta_paths: list[Path] = []
    paths = get_paths(url_or_paths=url_or_paths)
    for path in paths:
        if out_dir is None:
            meta_path: Path = path.with_stem(path.stem + meta_extension)
        else:
            meta_path = Path(os.path.join(out_dir, os.path.split(path)[1] + meta_extension))
            logger.info(f"Writing {meta_path}")
            _, content = parse_1(
                option=option,
                url_or_path=path,
                server_endpoint=server_endpoint,
                verbose=verbose,
                tika_server_jar=tika_server_jar,
                response_mime_type=response_mime_type,
                services=services,
            )

            if isinstance(content, str):
                content = (content + "\n").encode("utf-8")

            with open(meta_path, mode="wb", encoding="utf-8") as f:
                f.write(content)

        meta_paths.append(meta_path)
    return meta_paths


def parse(
    option: str,
    url_or_paths: Iterable[str | Path | BinaryIO],
    *,
    server_endpoint: str = SERVER_ENDPOINT,
    verbose: int = VERBOSE,
    tika_server_jar: Path = TIKA_SERVER_JAR,
    response_mime_type: str = "application/json",
    services: dict[str, str] | None = None,
    raw_response: bool = False,
) -> list[tuple[int, str | bytes | BinaryIO]]:
    """Parse files and extract metadata and/or text content using Tika.

    Args:
        option: Parsing option ('meta', 'text', or 'all').
        url_or_paths: Files to parse as URLs, paths, or file-like objects.
        server_endpoint: Tika server URL. Defaults to SERVER_ENDPOINT.
        verbose: Logging verbosity level. Defaults to VERBOSE.
        tika_server_jar: Path to Tika server JAR. Defaults to TIKA_SERVER_JAR.
        response_mime_type: Expected response format. Defaults to "application/json".
        services: Dict mapping options to service endpoints. Defaults to
                 {'meta': '/meta', 'text': '/tika', 'all': '/rmeta'}.
        raw_response: If True, return raw response content. Defaults to False.

    Returns:
        list[tuple[int, str | bytes | BinaryIO]]: List of tuples containing
        (HTTP status code, parsed content) for each processed file.
    """
    services = services or {"meta": "/meta", "text": "/tika", "all": "/rmeta"}
    return [
        parse_1(
            option=option,
            url_or_path=path,
            server_endpoint=server_endpoint,
            verbose=verbose,
            tika_server_jar=tika_server_jar,
            response_mime_type=response_mime_type,
            services=services,
            raw_response=raw_response,
        )
        for path in url_or_paths
    ]


def parse_1(
    option: str,
    url_or_path: str | Path | BinaryIO,
    *,
    server_endpoint: str = SERVER_ENDPOINT,
    verbose: int = VERBOSE,
    tika_server_jar: Path = TIKA_SERVER_JAR,
    response_mime_type: str = "application/json",
    services: dict[str, str] | None = None,
    raw_response: bool = False,
    headers: dict[str, Any] | None = None,
    config_path: str | None = None,
    request_options: dict[str, Any] | None = None,
) -> tuple[int, str | bytes | BinaryIO]:
    """Parse a single file and extract metadata and/or text content using Tika.

    Args:
        option: Parsing option ('meta', 'text', or 'all').
        url_or_path: File to parse as URL, path, or file-like object.
        server_endpoint: Tika server URL. Defaults to SERVER_ENDPOINT.
        verbose: Logging verbosity level. Defaults to VERBOSE.
        tika_server_jar: Path to Tika server JAR. Defaults to TIKA_SERVER_JAR.
        response_mime_type: Expected response format. Defaults to "application/json".
        services: Dict mapping options to service endpoints. Defaults to
                 {'meta': '/meta', 'text': '/tika', 'all': '/rmeta'}.
        raw_response: If True, return raw response content. Defaults to False.
        headers: Additional HTTP headers for request. Defaults to None.
        config_path: Path to Tika config file. Defaults to None.
        request_options: Additional request options. Defaults to None.

    Returns:
        tuple[int, str | bytes | BinaryIO]: Tuple containing HTTP status code and parsed content.
    """
    services = services or {"meta": "/meta", "text": "/tika", "all": "/rmeta/text"}
    request_options = request_options or {}
    headers = headers or {}

    path, file_type = get_remote_file(url_or_path, TIKA_FILES_PATH)
    headers.update(
        **{
            "Accept": response_mime_type,
            "Content-Disposition": make_content_disposition_header(path),
        }
    )

    if option not in services:
        logger.warning("config option must be one of meta, text, or all; using all.")
    service = services.get(option, services["all"])
    if service == "/tika":
        response_mime_type = "text/plain"
    headers.update(
        **{
            "Accept": response_mime_type,
            "Content-Disposition": make_content_disposition_header(path),
        }
    )
    with get_file_handle(path) as f:
        status, response = call_server(
            verb="put",
            server_endpoint=server_endpoint,
            service=service,
            data=f,
            headers=headers,
            verbose=verbose,
            tika_server_jar=tika_server_jar,
            config_path=config_path,
            raw_response=raw_response,
            request_options=request_options,
        )

    if file_type == "remote" and isinstance(path, Path):
        path.unlink()
    return (status, response)


def detect_lang(
    option: str,
    url_or_paths: Iterable[str | Path | BinaryIO],
    server_endpoint: str = SERVER_ENDPOINT,
    verbose: int = VERBOSE,
    tika_server_jar: Path = TIKA_SERVER_JAR,
    response_mime_type: str = "text/plain",
    services: dict[str, str] | None = None,
) -> list[tuple[int, str | bytes | BinaryIO]]:
    """Detect the language of files using Tika.

    Args:
        option: Detection option (usually 'file').
        url_or_paths: Files to analyze as URLs, paths, or file-like objects.
        server_endpoint: Tika server URL. Defaults to SERVER_ENDPOINT.
        verbose: Logging verbosity level. Defaults to VERBOSE.
        tika_server_jar: Path to Tika server JAR. Defaults to TIKA_SERVER_JAR.
        response_mime_type: Expected response format. Defaults to "text/plain".
        services: Dict mapping options to service endpoints. Defaults to
                 {'file': '/language/stream'}.

    Returns:
        list[tuple[int, str | bytes | BinaryIO]]: List of tuples containing
        (HTTP status code, detected language code) for each file.

    Note:
        Language codes are returned as ISO 639-1 two-letter codes (e.g., 'en' for English).
    """
    services = services or {"file": "/language/stream"}
    paths = get_paths(url_or_paths)
    return [
        detect_lang_1(option, path, server_endpoint, verbose, tika_server_jar, response_mime_type, services)
        for path in paths
    ]


def detect_lang_1(
    option: str,
    url_or_path: str | Path | BinaryIO,
    server_endpoint: str = SERVER_ENDPOINT,
    verbose: int = VERBOSE,
    tika_server_jar: Path = TIKA_SERVER_JAR,
    response_mime_type: str = "text/plain",
    services: dict[str, str] | None = None,
    request_options: dict[str, Any] | None = None,
) -> tuple[int, str | bytes | BinaryIO]:
    """Detect the language of a single file using Tika.

    Args:
        option: Detection option (usually 'file').
        url_or_path: File to analyze as URL, path, or file-like object.
        server_endpoint: Tika server URL. Defaults to SERVER_ENDPOINT.
        verbose: Logging verbosity level. Defaults to VERBOSE.
        tika_server_jar: Path to Tika server JAR. Defaults to TIKA_SERVER_JAR.
        response_mime_type: Expected response format. Defaults to "text/plain".
        services: Dict mapping options to service endpoints. Defaults to
                 {'file': '/language/stream'}.
        request_options: Additional request options. Defaults to None.

    Returns:
        tuple[int, str | bytes | BinaryIO]: Tuple containing HTTP status code
        and detected language code.

    Raises:
        TikaError: If the specified option is not valid.
    """
    services = services or {"file": "/language/stream"}
    request_options = request_options or {}
    path, mode = get_remote_file(url_or_path, TIKA_FILES_PATH)
    if option not in services:
        msg = f"Language option must be one of {services.keys()}"
        logger.exception(msg)
        raise TikaError(msg)
    service = services[option]
    status, response = call_server(
        verb="put",
        server_endpoint=server_endpoint,
        service=service,
        data=get_file_handle(path),
        headers={"Accept": response_mime_type},
        verbose=verbose,
        tika_server_jar=tika_server_jar,
        request_options=request_options,
    )
    return (status, response)


def detect_type(
    option: str,
    url_or_paths: Iterable[str | Path | BinaryIO],
    server_endpoint: str = SERVER_ENDPOINT,
    verbose: int = VERBOSE,
    tika_server_jar: Path = TIKA_SERVER_JAR,
    response_mime_type: str = "text/plain",
    services: dict[str, str] | None = None,
) -> list[tuple[int, str | bytes | BinaryIO]]:
    """Detect MIME types of files using Tika.

    Args:
        option: Detection option (usually 'type').
        url_or_paths: Files to analyze as URLs, paths, or file-like objects.
        server_endpoint: Tika server URL. Defaults to SERVER_ENDPOINT.
        verbose: Logging verbosity level. Defaults to VERBOSE.
        tika_server_jar: Path to Tika server JAR. Defaults to TIKA_SERVER_JAR.
        response_mime_type: Expected response format. Defaults to "text/plain".
        services: Dict mapping options to service endpoints. Defaults to
                 {'type': '/detect/stream'}.

    Returns:
        list[tuple[int, str | bytes | BinaryIO]]: List of tuples containing
        (HTTP status code, detected MIME type) for each file.
    """
    services = services or {"type": "/detect/stream"}
    paths = get_paths(url_or_paths)
    return [
        detect_type_1(
            option=option,
            url_or_path=path,
            server_endpoint=server_endpoint,
            verbose=verbose,
            tika_server_jar=tika_server_jar,
            response_mime_type=response_mime_type,
            services=services,
        )
        for path in paths
    ]


def detect_type_1(
    option: str,
    url_or_path: str | Path | BinaryIO,
    server_endpoint: str = SERVER_ENDPOINT,
    verbose: int = VERBOSE,
    tika_server_jar: Path = TIKA_SERVER_JAR,
    response_mime_type: str = "text/plain",
    services: dict[str, Any] | None = None,
    config_path: str | None = None,
    request_options: dict[str, Any] | None = None,
) -> tuple[int, str | bytes | BinaryIO]:
    """Detect MIME type of a single file using Tika.

    Args:
        option: Detection option (usually 'type').
        url_or_path: File to analyze as URL, path, or file-like object.
        server_endpoint: Tika server URL. Defaults to SERVER_ENDPOINT.
        verbose: Logging verbosity level. Defaults to VERBOSE.
        tika_server_jar: Path to Tika server JAR. Defaults to TIKA_SERVER_JAR.
        response_mime_type: Expected response format. Defaults to "text/plain".
        services: Dict mapping options to service endpoints. Defaults to
                 {'type': '/detect/stream'}.
        config_path: Path to Tika config file. Defaults to None.
        request_options: Additional request options. Defaults to None.

    Returns:
        tuple[int, str | bytes | BinaryIO]: Tuple containing HTTP status code
        and detected MIME type.

    Raises:
        TikaError: If the specified option is not valid.
    """
    services = services or {"type": "/detect/stream"}
    request_options = request_options or {}
    path, _ = get_remote_file(url_or_path, TIKA_FILES_PATH)
    if option not in services:
        msg = f"Detect option must be one of {services.keys()}"
        logger.exception(msg)
        raise TikaError(msg)
    service = services[option]

    status, response = call_server(
        verb="put",
        server_endpoint=server_endpoint,
        service=service,
        data=get_file_handle(path),
        headers={
            "Accept": response_mime_type,
            "Content-Disposition": make_content_disposition_header(path),
        },
        verbose=verbose,
        tika_server_jar=tika_server_jar,
        config_path=config_path,
        request_options=request_options,
    )
    if CSV_OUTPUT == 1:
        return (status, url_or_path.decode("UTF-8") + "," + response)  # type: ignore
    return (status, response)


def get_config(
    option: str,
    server_endpoint: str = SERVER_ENDPOINT,
    verbose: int = VERBOSE,
    tika_server_jar: Path = TIKA_SERVER_JAR,
    response_mime_type: str = "application/json",
    services: dict[str, str] | None = None,
    request_options: dict[str, Any] | None = None,
) -> tuple[int, str | bytes | BinaryIO]:
    """Retrieves configuration information from the Tika server.

    Makes a GET request to the Tika server to fetch configuration details about
    various server capabilities including parsers, detectors, and MIME types.

    Args:
        option: The configuration to retrieve. Must be one of:
            - "mime-types": List of supported MIME types
            - "detectors": Available content type detectors
            - "parsers": Available document parsers
        server_endpoint: URL of the Tika server. Defaults to SERVER_ENDPOINT.
        verbose: Level of logging verbosity. Defaults to VERBOSE.
        tika_server_jar: Path to the Tika server JAR file. Defaults to TIKA_SERVER_JAR.
        response_mime_type: Expected MIME type of the response. Defaults to "application/json".
        services: Optional dictionary mapping config options to their service endpoints.
            Defaults to:
            {
                "mime-types": "/mime-types",
                "detectors": "/detectors",
                "parsers": "/parsers/details"
            }
        request_options: Optional dictionary of additional request options.

    Returns:
        A tuple containing:
            - HTTP status code (int)
            - Server response (str, bytes, or BinaryIO) containing the requested configuration

    Raises:
        TikaError: If the server returns an error status
        ValueError: If an invalid option is specified
        RuntimeError: If the server cannot be contacted

    Example:
        >>> status, config = get_config("parsers")
        >>> if status == 200:
        ...     print(config)  # Print parser configuration
    """
    services = services or {"mime-types": "/mime-types", "detectors": "/detectors", "parsers": "/parsers/details"}
    request_options = request_options or {}
    if option not in services:
        die("config option must be one of mime-types, detectors, or parsers")
    service = services[option]
    status, response = call_server(
        verb="get",
        server_endpoint=server_endpoint,
        service=service,
        data=None,
        headers={"Accept": response_mime_type},
        verbose=verbose,
        tika_server_jar=tika_server_jar,
        request_options=request_options,
    )
    return (status, response)


def call_server(  # noqa: C901
    verb: str,
    server_endpoint: str,
    service: str,
    data: str | bytes | BinaryIO | None,
    *,
    headers: dict[str, Any],
    verbose: int = VERBOSE,
    tika_server_jar: Path = TIKA_SERVER_JAR,
    http_verbs: dict[str, Any] | None = None,
    classpath: str | None = None,
    raw_response: bool = False,
    config_path: str | None = None,
    request_options: dict[str, Any] | None = None,
) -> tuple[int, str | bytes | BinaryIO]:
    """Make an HTTP request to the Tika Server.

    Args:
        verb: HTTP method ('get', 'put', or 'post').
        server_endpoint: Base URL of Tika server.
        service: Service path to append to server_endpoint.
        data: Request payload. Can be None for GET requests.
        headers: Dictionary of HTTP headers to include.
        verbose: Logging verbosity level. Defaults to VERBOSE.
        tika_server_jar: Path to Tika server JAR. Defaults to TIKA_SERVER_JAR.
        http_verbs: Dict mapping verb strings to request functions.
                   Defaults to using requests.get/put/post.
        classpath: Additional classpath entries. Defaults to None.
        raw_response: If True, return raw response content. Defaults to False.
        config_path: Path to Tika configuration file. Defaults to None.
        request_options: Additional options for requests. Defaults to None.

    Returns:
        tuple[int, str | bytes | BinaryIO]: Tuple containing:
            - HTTP status code
            - Response content (decoded as UTF-8 unless raw_response is True)

    Raises:
        TikaError: If server endpoint URL is invalid or HTTP verb is unsupported.
        RuntimeError: If server cannot be contacted.

    Note:
        - Automatically starts Tika server if needed
        - Handles Windows-specific file reading behavior
        - Default timeout is 60 seconds
    """
    http_verbs = http_verbs or {"get": requests.get, "put": requests.put, "post": requests.post}
    request_options = request_options or {}
    parsed_url = urlparse(server_endpoint)
    server_host = parsed_url.hostname
    scheme: Literal["http", "https"] = parsed_url.scheme  # type: ignore

    port = parsed_url.port
    if not port or not isinstance(port, int):
        msg = f"Port not specified or is invalid in server endpoint URL '{server_endpoint}'."
        raise TikaError(msg)

    if not server_host:
        msg = f"Server host not specified in server endpoint URL '{server_endpoint}'."
        raise TikaError(msg)

    if scheme not in ["http", "https"]:
        msg = f"Scheme not specified or is invalid in server endpoint URL '{server_endpoint}'."
        raise TikaError(msg)

    if classpath is None:
        classpath = TIKA_SERVER_CLASSPATH

    global TIKA_CLIENT_ONLY
    if not TIKA_CLIENT_ONLY:
        server_endpoint = check_tika_server(
            scheme=scheme,
            server_host=server_host,
            port=str(port),
            tika_server_jar=tika_server_jar,
            classpath=classpath,
            config_path=config_path,
        )

    service_url = server_endpoint + service
    if verb not in http_verbs:
        msg = f"Tika Server call must be one of {http_verbs.keys()}"
        logger.exception(msg)
        raise TikaError(msg)
    verb_fn = http_verbs[verb]

    if IS_WINDOWS and hasattr(data, "read"):
        data = data.read()  # type: ignore

    encoded_data = data
    if isinstance(data, str):
        encoded_data = data.encode("utf-8")

    request_options_default = {"timeout": 60, "headers": headers, "verify": False}
    effective_request_options = request_options_default.copy()
    effective_request_options.update(request_options)

    resp: requests.Response = verb_fn(service_url, encoded_data, **effective_request_options)

    if verbose:
        logger.info(sys.stderr, "Request headers: ", headers)
        logger.info(sys.stderr, "Response headers: ", resp.headers)
    if resp.status_code != 200:
        logger.warning("Tika server returned status: %d", resp.status_code)

    resp.encoding = "utf-8"
    if raw_response:
        return (resp.status_code, resp.content)
    return (resp.status_code, resp.text)


def check_tika_server(
    scheme: Literal["http", "https"] = "http",
    server_host: str = SERVER_HOST,
    port: str = PORT,
    tika_server_jar: Path = TIKA_SERVER_JAR,
    classpath: str | None = None,
    config_path: str | None = None,
) -> str:
    """Check if Tika server is running and start it if necessary.

    Args:
        scheme: Protocol to use ('http' or 'https'). Defaults to "http".
        server_host: Host where server should run. Defaults to SERVER_HOST.
        port: Port for the server. Defaults to PORT.
        tika_server_jar: Path to Tika server JAR. Defaults to TIKA_SERVER_JAR.
        classpath: Additional classpath entries. Defaults to None.
        config_path: Path to Tika configuration file. Defaults to None.

    Returns:
        str: Server endpoint URL (e.g., "http://localhost:9998")

    Raises:
        RuntimeError: If server JAR signature doesn't match or server fails to start.

    Note:
        Only attempts to start server for localhost or 127.0.0.1 addresses.
        For remote servers, just returns the endpoint URL.
    """
    if classpath is None:
        classpath = TIKA_SERVER_CLASSPATH
    if port is None:
        port = "443" if scheme == "https" else "80"

    server_endpoint = f"{scheme}://{server_host}:{port}"
    jar_path = Path(os.path.join(TIKA_JAR_PATH, "tika-server.jar"))
    if "localhost" in server_endpoint or "127.0.0.1" in server_endpoint:
        already_running = check_port_is_open(remote_server_host=server_host, port=port)

        if not already_running:
            if not check_jar_signature(tika_server_jar=tika_server_jar, jar_path=jar_path):
                msg = f"Jar signature does not match for JAR {tika_server_jar} at path {jar_path}"
                logger.error(msg)
                raise RuntimeError(msg)

            status = start_server(
                tika_server_jar=jar_path,
                java_path=TIKA_JAVA,
                java_args=TIKA_JAVA_ARGS,
                server_host=server_host,
                port=port,
                classpath=classpath,
                config_path=config_path,
            )
            if not status:
                logger.error("Failed to receive startup confirmation from startServer.")
                msg = "Unable to start Tika server."
                raise RuntimeError(msg)
    return server_endpoint


def check_jar_signature(tika_server_jar: Path, jar_path: Path) -> bool:
    """
    Checks the signature of Jar
    :param tika_server_jar:
    :param jarPath:
    :return: ``True`` if the signature of the jar matches
    """
    local_checksum_path = Path(jar_path, TIKA_JAR_HASH_ALGO)
    if not local_checksum_path.exists():
        msg = f"Checksum file not found for JAR {tika_server_jar} at path {jar_path}"
        raise RuntimeError(msg)

    m = hashlib.new(TIKA_JAR_HASH_ALGO)

    with open(jar_path, "rb") as f:
        bin_contents = f.read()
        m.update(bin_contents)
        with open(local_checksum_path) as em:
            existing_contents = em.read()
            return existing_contents == m.hexdigest()


def start_server(  # noqa: C901
    tika_server_jar: Path,
    java_path: str = TIKA_JAVA,
    java_args: str = TIKA_JAVA_ARGS,
    server_host: str = SERVER_HOST,
    port: str = PORT,
    classpath: str | None = None,
    config_path: str | None = None,
) -> bool:
    """Start the Tika Server as a subprocess.

    Args:
        tika_server_jar: Path to the Tika server JAR file.
        java_path: Path to Java executable. Defaults to TIKA_JAVA.
        java_args: Additional Java arguments. Defaults to TIKA_JAVA_ARGS.
        server_host: Host interface address for binding. Defaults to SERVER_HOST.
        port: Port number for the server. Defaults to PORT.
        classpath: Additional classpath entries. Defaults to None.
        config_path: Path to Tika configuration file. Defaults to None.

    Returns:
        bool: True if server started successfully, False otherwise.

    Note:
        - Creates a log file at TIKA_SERVER_LOG_FILE_PATH/tika-server.log
        - On Windows, forces server_host to "0.0.0.0"
        - Attempts to start server multiple times based on TIKA_STARTUP_MAX_RETRY
        - Sets global TIKA_SERVER_PROCESS variable for later cleanup
    """
    if classpath is None:
        classpath = TIKA_SERVER_CLASSPATH

    if IS_WINDOWS:
        server_host = "0.0.0.0"  # noqa: S104

    if classpath:
        if IS_WINDOWS:
            classpath += ";" + str(tika_server_jar)
            classpath = '"' + classpath + '"'
        else:
            classpath += ":" + str(tika_server_jar)
    else:
        classpath = str(tika_server_jar)

    # setup command string
    cmd_string = ""
    if not config_path:
        cmd_string = f'{java_path} {java_args} -cp "{classpath}" org.apache.tika.server.core.TikaServerCli --port {port} --host {server_host} &'  # noqa: E501
    else:
        cmd_string = f'{java_path} {java_args} -cp "{classpath}" org.apache.tika.server.core.TikaServerCli --port {port} --host {server_host} --config {config_path} &'  # noqa: E501

    # Check that we can write to log path
    try:
        tika_log_file_path = os.path.join(TIKA_SERVER_LOG_FILE_PATH, "tika-server.log")
        log_file = open(tika_log_file_path, "w")  # noqa: SIM115
        logger.info(f"Logging to {tika_log_file_path}")
    except PermissionError:
        logger.error(f"Unable to create tika-server.log at {TIKA_SERVER_LOG_FILE_PATH} due to permission error.")
        return False

    # Check that specified java binary is available on path
    try:
        _ = Popen(java_path, stdout=open(os.devnull, "w"), stderr=open(os.devnull, "w"))  # noqa: S603, SIM115
    except FileNotFoundError:
        logger.error("Unable to run java; is it installed?")
        return False

    # Run java with jar args
    global TIKA_SERVER_PROCESS
    # Patch for Windows support
    if IS_WINDOWS:
        if sys.version.startswith("2"):
            # Python 2.x
            TIKA_SERVER_PROCESS = Popen(cmd_string, stdout=log_file, stderr=STDOUT, shell=True)  # noqa: S602
        elif sys.version.startswith("3"):
            # Python 3.x
            TIKA_SERVER_PROCESS = Popen(cmd_string, stdout=log_file, stderr=STDOUT, shell=True, start_new_session=True)  # noqa: S602
    else:
        TIKA_SERVER_PROCESS = Popen(cmd_string, stdout=log_file, stderr=STDOUT, shell=True, preexec_fn=os.setsid)  # noqa: S602

    # Check logs and retry as configured
    try_count = 0
    is_started = False
    while try_count < TIKA_STARTUP_MAX_RETRY:
        with open(tika_log_file_path) as tika_log_file_tmp:
            # check for INFO string to confirm listening endpoint
            if "Started Apache Tika server" in tika_log_file_tmp.read():
                is_started = True
                break
            logger.warning("Failed to see startup log message; retrying...")
        time.sleep(TIKA_STARTUP_SLEEP)
        try_count += 1

    if not is_started:
        logger.error("Tika startup log message not received after %d tries." % (TIKA_STARTUP_MAX_RETRY))  # noqa: UP031
        return False
    return True


def kill_server(
    tika_server_process: Popen | None = None,
    *,
    is_windows: bool = False,
) -> None:
    """Kill the running Tika server process.

    Args:
        tika_server_process: The subprocess.Popen instance of the Tika server.
                           If None, logs an error. Defaults to None.
        is_windows: Boolean flag indicating if running on Windows platform.
                   Defaults to False.

    Note:
        - On Windows, uses SIGTERM signal directly
        - On Unix-like systems, kills the process group
        - Waits 1 second after sending kill signal
        - Logs errors if process cannot be killed
    """
    if tika_server_process is None:
        logger.error("Server not running, or was already running before")
        return

    try:
        if is_windows:
            os.kill(tika_server_process.pid, signal.SIGTERM)
        else:
            os.killpg(os.getpgid(tika_server_process.pid), signal.SIGTERM)
    except (ProcessLookupError, OSError) as e:
        logger.error("Failed to kill the current server session: %s", str(e))
    finally:
        time.sleep(1)


def to_filename(url: str) -> str:
    """
    Gets url and returns filename
    """
    urlp = urlparse(url)
    path = urlp.path
    if not path:
        path = f"file_{int(time.time())}"
    value = re.sub(r"[^\w\s\.\-]", "-", path).strip().lower()
    return re.sub(r"[-\s]+", "-", value).strip("-")[-200:]


def get_file_handle(url_or_path: str | Path | BinaryIO) -> BinaryIO:
    """
    Opens a remote file and returns a file-like object.

    Args:
        url_or_path: resource locator, generally URL or path, or file object

    Returns:
        file-like object
    """
    if isinstance(url_or_path, Path):
        return open(url_or_path, "rb")
    if isinstance(url_or_path, BinaryIO):
        return url_or_path
    return open(url_or_path, "rb")


def get_remote_file(
    url_or_path: str | Path | BinaryIO,
    dest_path: str | Path,
) -> tuple[Path, Literal["local", "remote", "binary"]]:
    """Fetch a remote file or handle a local file/binary stream.

    Args:
        url_or_path: Resource to fetch - can be a URL, local path, or file-like object.
        dest_path: Local path where to save the file if it needs to be downloaded.

    Returns:
        tuple[Path, Literal["local", "remote", "binary"]]: Tuple containing:
            - Path object pointing to the local file
            - String indicating the source type: "local" for local files,
              "remote" for downloaded files, "binary" for binary streams

    Raises:
        TikaError: If a local file does not exist.
        OSError: If there are issues downloading a remote file.

    Note:
        For binary stream inputs, a temporary file is created with a timestamp-based name.
    """
    # handle binary stream input
    if not isinstance(url_or_path, Path | str):
        name = f"file_{int(time.time())}" if not hasattr(url_or_path, "name") else url_or_path.name
        filename = to_filename(name)
        dest_path = Path(dest_path) / filename
        with open(dest_path, "wb") as f:
            f.write(url_or_path.read())
        return (dest_path, "binary")

    if isinstance(url_or_path, Path):
        return (url_or_path, "local")

    urlp = urlparse(url_or_path)
    if urlp.scheme == "":
        path = Path(url_or_path)
        if not path.exists():
            msg = f"File {path} does not exist."
            raise TikaError(msg)
        return (path, "local")
    filename = to_filename(url_or_path)  # Assuming to_filename exists and returns str
    dest_path = Path(dest_path) / filename
    logger.info("Retrieving %s to %s.", url_or_path, dest_path)
    try:
        urlretrieve(url_or_path, dest_path)  # noqa: S310
    except OSError:
        # monkey patch fix for SSL/Windows per Tika-Python #54
        # https://github.com/chrismattmann/tika-python/issues/54
        import ssl

        if hasattr(ssl, "_create_unverified_context"):
            ssl._create_default_https_context = ssl._create_unverified_context
        # delete whatever we had there
        if os.path.exists(dest_path) and os.path.isfile(dest_path):
            os.remove(dest_path)
        urlretrieve(url_or_path, dest_path)  # noqa: S310
    return (dest_path, "remote")


def check_port_is_open(
    remote_server_host: str = SERVER_HOST,
    port: str = PORT,
) -> bool:
    """Check if a specific port is open on the given host.

    Args:
        remote_server_host: Hostname to check. Defaults to SERVER_HOST.
        port: Port number to check. Defaults to PORT.

    Returns:
        bool: True if the port is open and accepting connections, False otherwise.

    Note:
        This function will exit the program if:
            - There is a keyboard interrupt
            - The hostname cannot be resolved
            - There are connection issues with the server
    """
    remote_server_ip = socket.gethostbyname(remote_server_host)

    sock: socket.socket | None = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remote_server_ip, int(port)))
        return result == 0

    except KeyboardInterrupt:
        logger.info("You pressed Ctrl+C")
        sys.exit()

    except socket.gaierror:
        logger.info("Hostname could not be resolved. Exiting")
        sys.exit()

    except OSError:
        logger.info("Couldn't connect to server")
        sys.exit()

    finally:
        if sock:
            sock.close()


def main(argv: Any = None) -> list[Path] | list[tuple[int, str | bytes | BinaryIO]] | str | bytes | BinaryIO:  # noqa: ANN401, C901
    """Run Tika from command line according to USAGE."""
    global VERBOSE
    global ENCODE_UTF8
    global CSV_OUTPUT
    if argv is None:
        argv = sys.argv

    if len(argv) < 3 and not (("-h" in argv) or ("--help" in argv)):
        msg = "Bad args"
        logger.exception(msg)
        raise TikaError(msg)
    try:
        opts, argv = getopt.getopt(
            argv[1:], "hi:s:o:p:v:e:c", ["help", "install=", "server=", "output=", "port=", "verbose", "encode", "csv"]
        )
    except getopt.GetoptError as opt_error:
        msg, bad_opt = opt_error  # type: ignore
        msg = f"{argv[0]} error: Bad option: {bad_opt}, {msg}"
        logger.exception(msg)
        raise TikaError from opt_error

    tika_server_jar = TIKA_SERVER_JAR
    server_host = SERVER_HOST
    out_dir = Path(".")
    port = PORT
    for opt, val in opts:
        if opt in ("-h", "--help"):
            echo2(USAGE)
            sys.exit()
        elif opt in ("--install"):
            tika_server_jar = Path(val)
        elif opt in ("--server"):
            server_host = val
        elif opt in ("-o", "--output"):
            out_dir = Path(val)
        elif opt in ("--port"):
            port = val
        elif opt in ("-v", "--verbose"):
            VERBOSE = 1
        elif opt in ("-e", "--encode"):
            ENCODE_UTF8 = 1
        elif opt in ("-c", "--csv"):
            CSV_OUTPUT = 1
        else:
            raise TikaError(USAGE)

    cmd = argv[0]
    option = argv[1]
    try:
        paths = argv[2:]
    except:  # noqa: E722
        paths = None
    return run_command(
        cmd=cmd,
        option=option,
        url_or_paths=paths,  # type: ignore
        port=port,
        out_dir=out_dir,
        server_host=server_host,
        tika_server_jar=tika_server_jar,
        verbose=VERBOSE,
        encode=ENCODE_UTF8,
    )


if __name__ == "__main__":
    logger.info(f"Logging on '{LOG_FILE}'")
    resp = main(sys.argv)

    out: codecs.StreamWriter
    # Set encoding of the terminal to UTF-8
    if sys.version.startswith("2"):
        # Python 2.x
        out: codecs.StreamWriter = codecs.getwriter("UTF-8")(sys.stdout)  # type: ignore
    elif sys.version.startswith("3"):
        # Python 3.x
        out = codecs.getwriter("UTF-8")(sys.stdout.buffer)
    else:
        msg = "Unsupported Python version"
        raise TikaError(msg)

    if type(resp) is list:
        out.write("\n".join([r[1] for r in resp]))  # type: ignore
    elif type(resp) is str:
        out.write(resp)
    else:
        msg = "Bad response type"
        raise TikaError(msg)
    out.write("\n")
