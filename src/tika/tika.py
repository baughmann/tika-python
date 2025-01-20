#!/usr/bin/env python
# encoding: utf-8
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

**Use Tika Translate**::

   from tika import translate
   print(translate.from_file('/path/to/file', 'srcLang', 'destLang')
   # Use auto Language detection feature
   print(translate.from_file('/path/to/file', 'destLang')

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
import ctypes
import getopt
import hashlib
import io
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

"""


class TikaResponse(TypedDict):
    status: int
    metadata: dict[str, str | list[str]] | None
    content: str | bytes | BinaryIO | None


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

    def make_content_disposition_header(fn):
        return build_header(os.path.basename(fn)).decode("ascii")
except ImportError:

    def make_content_disposition_header(fn):
        return "attachment; filename=%s" % os.path.basename(fn)


if sys.version_info[0] < 3:
    open = codecs.open


LOG_DIR = Path(os.getenv("TIKA_LOG_PATH", tempfile.gettempdir()))
LOG_FILE = Path(os.path.join(LOG_DIR, os.getenv("TIKA_LOG_FILE", "tika.log")))

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
log: logging.Logger = logging.getLogger("tika.tika")

if os.getenv("TIKA_LOG_FILE", "tika.log"):
    # File logs
    fileHandler = logging.FileHandler(LOG_FILE)
    fileHandler.setFormatter(logFormatter)
    log.addHandler(fileHandler)

    # Stdout logs
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    log.addHandler(consoleHandler)

# Log level
log.setLevel(logging.INFO)

IS_WINDOWS = True if platform.system() == "Windows" else False
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
TikaServerJar = Path(os.getenv("TIKA_SERVER_JAR", get_bundled_jar_path()))

SERVER_HOST = "localhost"
PORT = "9998"
SERVER_ENDPOINT: str = os.getenv("TIKA_SERVER_ENDPOINT", "http://" + SERVER_HOST + ":" + PORT)
TRANSLATOR: str = os.getenv("TIKA_TRANSLATOR", "org.apache.tika.language.translate.Lingo24Translator")
TIKA_CLIENT_ONLY = bool(os.getenv("TIKA_CLIENT_ONLY", False))
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


class TikaException(Exception):
    pass


def echo2(*s) -> types.NoneType:
    sys.stderr.write(unicode_string("tika.py: %s\n") % unicode_string(" ").join(map(unicode_string, s)))


def warn(*s) -> types.NoneType:
    echo2("Warn:", *s)


def die(*s) -> NoReturn:
    warn("Error:", *s)
    echo2(USAGE)
    sys.exit()


def run_command(
    cmd: str,
    option: str,
    urlOrPaths,
    port: str,
    outDir: Path | None = None,
    serverHost: str = SERVER_HOST,
    tikaServerJar: Path = TikaServerJar,
    verbose: int = VERBOSE,
    encode: int = ENCODE_UTF8,
) -> list[Path] | list[tuple[int, str | bytes | BinaryIO]] | str | bytes | BinaryIO:
    """
    Run the Tika command by calling the Tika server and return results in JSON format (or plain text).
    :param cmd: a command from set ``{'parse', 'detect', 'language', 'translate', 'config'}``
    :param option:
    :param urlOrPaths:
    :param port:
    :param outDir:
    :param serverHost:
    :param tikaServerJar:
    :param verbose:
    :param encode:
    :return: response for the command, usually a ``dict``
    """
    # import pdb; pdb.set_trace()
    if (cmd in "parse" or cmd in "detect") and not urlOrPaths:
        log.exception("No URLs/paths specified.")
        raise TikaException("No URLs/paths specified.")
    server_endpoint = "http://" + serverHost + ":" + port
    if cmd == "parse":
        return parse_and_save(option, urlOrPaths, outDir, server_endpoint, verbose, tikaServerJar)
    elif cmd == "detect":
        return detect_type(option, urlOrPaths, server_endpoint, verbose, tikaServerJar)
    elif cmd == "language":
        return detect_lang(option, urlOrPaths, server_endpoint, verbose, tikaServerJar)
    elif cmd == "translate":
        return do_translate(option, urlOrPaths, server_endpoint, verbose, tikaServerJar)
    elif cmd == "config":
        status, resp = get_config(option, server_endpoint, verbose, tikaServerJar)
        return resp
    else:
        log.exception("Bad args")
        raise TikaException("Bad args")


def get_paths(urlOrPaths) -> list[Path]:
    """
    Determines if the given URL in urlOrPaths is a URL or a file or directory. If it's
    a directory, it walks the directory and then finds all file paths in it, and ads them
    too. If it's a file, it adds it to the paths. If it's a URL it just adds it to the path.
    :param urlOrPaths: the url or path to be scanned
    :return: ``list`` of paths
    """
    if isinstance(urlOrPaths, unicode_string):
        urlOrPaths = [urlOrPaths]  # do not recursively walk over letters of a single path which can include "/"
    paths = []
    for eachUrlOrPaths in urlOrPaths:
        if os.path.isdir(eachUrlOrPaths):
            for root, directories, filenames in walk(eachUrlOrPaths):
                for filename in filenames:
                    paths.append(os.path.join(root, filename))
        else:
            paths.append(eachUrlOrPaths)
    return paths


def parse_and_save(
    option: str,
    urlOrPaths,
    outDir=None,
    server_endpoint=SERVER_ENDPOINT,
    verbose=VERBOSE,
    tikaServerJar=TikaServerJar,
    responseMimeType="application/json",
    metaExtension="_meta.json",
    services={"meta": "/meta", "text": "/tika", "all": "/rmeta"},
) -> list[Path]:
    """
    Parse the objects and write extracted metadata and/or text in JSON format to matching
    filename with an extension of '_meta.json'.
    :param option:
    :param urlOrPaths:
    :param outDir:
    :param server_endpoint:
    :param verbose:
    :param tikaServerJar:
    :param responseMimeType:
    :param metaExtension:
    :param services:
    :return:
    """
    metaPaths: list[Path] = []
    paths = get_paths(urlOrPaths=urlOrPaths)
    for path in paths:
        if outDir is None:
            metaPath: Path = path.with_stem(path.stem + metaExtension)
        else:
            metaPath = Path(os.path.join(outDir, os.path.split(path)[1] + metaExtension))
            log.info("Writing %s" % metaPath)
            _, content = parse_1(
                option=option,
                urlOrPath=path,
                server_endpoint=server_endpoint,
                verbose=verbose,
                tikaServerJar=tikaServerJar,
                responseMimeType=responseMimeType,
                services=services,
            )

            if isinstance(content, str):
                content = (content + "\n").encode("utf-8")

            with open(metaPath, mode="wb", encoding="utf-8") as f:
                f.write(content)

        metaPaths.append(metaPath)
    return metaPaths


def parse(
    option: str,
    urlOrPaths,
    server_endpoint: str = SERVER_ENDPOINT,
    verbose: int = VERBOSE,
    tikaServerJar: Path = TikaServerJar,
    responseMimeType: str = "application/json",
    services: dict[str, str] | None = None,
    rawResponse: bool = False,
) -> list[tuple[int, str | bytes | BinaryIO]]:
    """
    Parse the objects and return extracted metadata and/or text in JSON format.
    :param option:
    :param urlOrPaths:
    :param server_endpoint:
    :param verbose:
    :param tikaServerJar:
    :param responseMimeType:
    :param services:
    :return:
    """
    services = services or {"meta": "/meta", "text": "/tika", "all": "/rmeta"}
    return [
        parse_1(
            option=option,
            urlOrPath=path,
            server_endpoint=server_endpoint,
            verbose=verbose,
            tikaServerJar=tikaServerJar,
            responseMimeType=responseMimeType,
            services=services,
            rawResponse=rawResponse,
        )
        for path in urlOrPaths
    ]


def parse_1(
    option: str,
    urlOrPath,
    server_endpoint=SERVER_ENDPOINT,
    verbose: int = VERBOSE,
    tikaServerJar=TikaServerJar,
    responseMimeType="application/json",
    services={"meta": "/meta", "text": "/tika", "all": "/rmeta/text"},
    rawResponse: bool = False,
    headers: dict[str, Any] | None = None,
    config_path: str | None = None,
    request_options: dict[str, Any] | None = None,
) -> tuple[int, str | bytes | BinaryIO]:
    """
    Parse the object and return extracted metadata and/or text in JSON format.
    :param option:
    :param urlOrPath:
    :param server_endpoint:
    :param verbose:
    :param tikaServerJar:
    :param responseMimeType:
    :param services:
    :param rawResponse:
    :param headers:
    :return:
    """
    request_options = request_options or {}
    headers = headers or {}

    path, file_type = get_remote_file(urlOrPath, TIKA_FILES_PATH)
    headers.update(
        {
            "Accept": responseMimeType,
            "Content-Disposition": make_content_disposition_header(
                path.encode("utf-8") if isinstance(path, str) else path
            ),
        }
    )

    if option not in services:
        log.warning("config option must be one of meta, text, or all; using all.")
    service = services.get(option, services["all"])
    if service == "/tika":
        responseMimeType = "text/plain"
    headers.update(
        {
            "Accept": responseMimeType,
            "Content-Disposition": make_content_disposition_header(
                path.encode("utf-8") if isinstance(path, str) else path
            ),
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
            tikaServerJar=tikaServerJar,
            config_path=config_path,
            rawResponse=rawResponse,
            request_options=request_options,
        )

    if file_type == "remote" and isinstance(path, Path):
        path.unlink()
    return (status, response)


def detect_lang(
    option: str,
    urlOrPaths,
    server_endpoint: str = SERVER_ENDPOINT,
    verbose: int = VERBOSE,
    tikaServerJar=TikaServerJar,
    responseMimeType: str = "text/plain",
    services: dict[str, str] | None = None,
) -> list[tuple[int, str | bytes | BinaryIO]]:
    """
    Detect the language of the provided stream and return its 2 character code as text/plain.
    :param option:
    :param urlOrPaths:
    :param server_endpoint:
    :param verbose:
    :param tikaServerJar:
    :param responseMimeType:
    :param services:
    :return:
    """
    services = services or {"file": "/language/stream"}
    paths = get_paths(urlOrPaths)
    return [
        detect_lang_1(option, path, server_endpoint, verbose, tikaServerJar, responseMimeType, services)
        for path in paths
    ]


def detect_lang_1(
    option: str,
    urlOrPath,
    server_endpoint: str = SERVER_ENDPOINT,
    verbose: int = VERBOSE,
    tikaServerJar=TikaServerJar,
    responseMimeType: str = "text/plain",
    services: dict[str, str] | None = None,
    request_options: dict[str, Any] | None = None,
) -> tuple[int, str | bytes | BinaryIO]:
    """
    Detect the language of the provided stream and return its 2 character code as text/plain.
    :param option:
    :param urlOrPath:
    :param server_endpoint:
    :param verbose:
    :param tikaServerJar:
    :param responseMimeType:
    :param services:
    :return:
    """
    services = services or {"file": "/language/stream"}
    request_options = request_options or {}
    path, mode = get_remote_file(urlOrPath, TIKA_FILES_PATH)
    if option not in services:
        msg = f"Language option must be one of {services.keys()}"
        log.exception(msg)
        raise TikaException(msg)
    service = services[option]
    status, response = call_server(
        verb="put",
        server_endpoint=server_endpoint,
        service=service,
        data=get_file_handle(path),
        headers={"Accept": responseMimeType},
        verbose=verbose,
        tikaServerJar=tikaServerJar,
        request_options=request_options,
    )
    return (status, response)


def do_translate(
    option: str,
    urlOrPaths,
    server_endpoint: str = SERVER_ENDPOINT,
    verbose: int = VERBOSE,
    tikaServerJar=TikaServerJar,
    responseMimeType: str = "text/plain",
    services: dict[str, str] | None = None,
) -> list[tuple[int, str | bytes | BinaryIO]]:
    """
    Translate the file from source language to destination language.
    :param option:
    :param urlOrPaths:
    :param server_endpoint:
    :param verbose:
    :param tikaServerJar:
    :param responseMimeType:
    :param services:
    :return:
    """
    services = services or {"all": "/translate/all"}
    paths = get_paths(urlOrPaths)
    return [
        do_translate_1(option, path, server_endpoint, verbose, tikaServerJar, responseMimeType, services)
        for path in paths
    ]


def do_translate_1(
    option: str,
    urlOrPath,
    server_endpoint: str = SERVER_ENDPOINT,
    verbose: int = VERBOSE,
    tikaServerJar=TikaServerJar,
    responseMimeType: str = "text/plain",
    services: dict[str, str] | None = None,
    request_options: dict[str, Any] | None = None,
) -> tuple[int, str | bytes | BinaryIO]:
    """

    :param option:
    :param urlOrPath:
    :param server_endpoint:
    :param verbose:
    :param tikaServerJar:
    :param responseMimeType:
    :param services:
    :return:
    """
    services = services or {"all": "/translate/all"}
    request_options = request_options or {}
    path, mode = get_remote_file(urlOrPath, TIKA_FILES_PATH)
    srcLang = ""
    destLang = ""

    if ":" in option:
        options = option.rsplit(":")
        srcLang = options[0]
        destLang = options[1]
        if len(options) != 2:
            log.exception("Translate options are specified as srcLang:destLang or as destLang")
            raise TikaException("Translate options are specified as srcLang:destLang or as destLang")
    else:
        destLang = option

    if srcLang != "" and destLang != "":
        service = services["all"] + "/" + TRANSLATOR + "/" + srcLang + "/" + destLang
    else:
        service = services["all"] + "/" + TRANSLATOR + "/" + destLang
    status, response = call_server(
        verb="put",
        server_endpoint=server_endpoint,
        service=service,
        data=get_file_handle(path),
        headers={"Accept": responseMimeType},
        verbose=verbose,
        tikaServerJar=tikaServerJar,
        request_options=request_options,
    )
    return (status, response)


def detect_type(
    option: str,
    urlOrPaths,
    server_endpoint: str = SERVER_ENDPOINT,
    verbose: int = VERBOSE,
    tikaServerJar=TikaServerJar,
    responseMimeType: str = "text/plain",
    services: dict[str, str] | None = None,
) -> list[tuple[int, str | bytes | BinaryIO]]:
    """
    Detect the MIME/media type of the stream and return it in text/plain.
    :param option:
    :param urlOrPaths:
    :param server_endpoint:
    :param verbose:
    :param tikaServerJar:
    :param responseMimeType:
    :param services:
    :return:
    """
    services = services or {"type": "/detect/stream"}
    paths = get_paths(urlOrPaths)
    return [
        detect_type_1(option, path, server_endpoint, verbose, tikaServerJar, responseMimeType, services)
        for path in paths
    ]


def detect_type_1(
    option: str,
    urlOrPath,
    server_endpoint: str = SERVER_ENDPOINT,
    verbose: int = VERBOSE,
    tikaServerJar: Path = TikaServerJar,
    responseMimeType: str = "text/plain",
    services: dict[str, Any] | None = None,
    config_path: str | None = None,
    request_options: dict[str, Any] | None = None,
) -> tuple[int, str | bytes | BinaryIO]:
    """
    Detect the MIME/media type of the stream and return it in text/plain.
    :param option:
    :param urlOrPath:
    :param server_endpoint:
    :param verbose:
    :param tikaServerJar:
    :param responseMimeType:
    :param services:
    :return:
    """
    services = services or {"type": "/detect/stream"}
    request_options = request_options or {}
    path, _ = get_remote_file(urlOrPath, TIKA_FILES_PATH)
    if option not in services:
        msg = f"Detect option must be one of {services.keys()}"
        log.exception(msg)
        raise TikaException(msg)
    service = services[option]

    status, response = call_server(
        verb="put",
        server_endpoint=server_endpoint,
        service=service,
        data=get_file_handle(path),
        headers={
            "Accept": responseMimeType,
            "Content-Disposition": make_content_disposition_header(
                path.encode("utf-8") if isinstance(path, str) else path
            ),
        },
        verbose=verbose,
        tikaServerJar=tikaServerJar,
        config_path=config_path,
        request_options=request_options,
    )
    if CSV_OUTPUT == 1:
        return (status, urlOrPath.decode("UTF-8") + "," + response)
    else:
        return (status, response)


def get_config(
    option: str,
    server_endpoint: str = SERVER_ENDPOINT,
    verbose: int = VERBOSE,
    tikaServerJar=TikaServerJar,
    responseMimeType="application/json",
    services={"mime-types": "/mime-types", "detectors": "/detectors", "parsers": "/parsers/details"},
    request_options: dict[str, Any] | None = None,
) -> tuple[int, str | bytes | BinaryIO]:
    """
    Get the configuration of the Tika Server (parsers, detectors, etc.) and return it in JSON format.
    :param option:
    :param server_endpoint:
    :param verbose:
    :param tikaServerJar:
    :param responseMimeType:
    :param services:
    :return:
    """
    request_options = request_options or {}
    if option not in services:
        die("config option must be one of mime-types, detectors, or parsers")
    service = services[option]
    status, response = call_server(
        verb="get",
        server_endpoint=server_endpoint,
        service=service,
        data=None,
        headers={"Accept": responseMimeType},
        verbose=verbose,
        tikaServerJar=tikaServerJar,
        request_options=request_options,
    )
    return (status, response)


def call_server(
    verb: str,
    server_endpoint: str,
    service: str,
    data: str | bytes | BinaryIO | None,
    headers: dict[str, Any],
    verbose: int = VERBOSE,
    tikaServerJar: Path = TikaServerJar,
    httpVerbs={"get": requests.get, "put": requests.put, "post": requests.post},
    classpath=None,
    rawResponse: bool = False,
    config_path: str | None = None,
    request_options: dict[str, Any] | None = None,
) -> tuple[int, str | bytes | BinaryIO]:
    """
    Call the Tika Server, do some error checking, and return the response.
    :param verb:
    :param server_endpoint:
    :param service:
    :param data:
    :param headers:
    :param verbose:
    :param tikaServerJar:
    :param httpVerbs:
    :param classpath:
    :return:
    """
    request_options = request_options or {}
    parsedUrl = urlparse(server_endpoint)
    serverHost = parsedUrl.hostname
    scheme: Literal["http", "https"] = parsedUrl.scheme  # type: ignore

    port = parsedUrl.port
    if not port or not isinstance(port, int):
        raise TikaException(f"Port not specified or is invalid in server endpoint URL '{server_endpoint}'.")

    if not serverHost:
        raise TikaException(f"Server host not specified in server endpoint URL '{server_endpoint}'.")

    if scheme not in ["http", "https"]:
        raise TikaException(f"Scheme not specified or is invalid in server endpoint URL '{server_endpoint}'.")

    if classpath is None:
        classpath = TIKA_SERVER_CLASSPATH

    global TIKA_CLIENT_ONLY
    if not TIKA_CLIENT_ONLY:
        server_endpoint = check_tika_server(
            scheme=scheme,
            serverHost=serverHost,
            port=str(port),
            tikaServerJar=tikaServerJar,
            classpath=classpath,
            config_path=config_path,
        )

    serviceUrl = server_endpoint + service
    if verb not in httpVerbs:
        log.exception("Tika Server call must be one of %s" % binary_string(httpVerbs.keys()))
        raise TikaException("Tika Server call must be one of %s" % binary_string(httpVerbs.keys()))
    verbFn = httpVerbs[verb]

    if IS_WINDOWS and hasattr(data, "read"):
        data = data.read()  # type: ignore

    encodedData = data
    if isinstance(data, str):
        encodedData = data.encode("utf-8")

    request_optionsDefault = {"timeout": 60, "headers": headers, "verify": False}
    effective_request_options = request_optionsDefault.copy()
    effective_request_options.update(request_options)

    resp: requests.Response = verbFn(serviceUrl, encodedData, **effective_request_options)

    if verbose:
        print(sys.stderr, "Request headers: ", headers)
        print(sys.stderr, "Response headers: ", resp.headers)
    if resp.status_code != 200:
        log.warning("Tika server returned status: %d", resp.status_code)

    resp.encoding = "utf-8"
    if rawResponse:
        return (resp.status_code, resp.content)
    else:
        return (resp.status_code, resp.text)


def check_tika_server(
    scheme: Literal["http", "https"] = "http",
    serverHost: str = SERVER_HOST,
    port: str = PORT,
    tikaServerJar=TikaServerJar,
    classpath: str | None = None,
    config_path=None,
) -> str:
    """
    Check that tika-server is running.  If not, download JAR file and start it up.
    :param scheme: e.g. http or https
    :param serverHost:
    :param port:
    :param tikaServerJar:
    :param classpath:
    :return:
    """
    if classpath is None:
        classpath = TIKA_SERVER_CLASSPATH
    if port is None:
        port = "443" if scheme == "https" else "80"

    server_endpoint = "%s://%s:%s" % (scheme, serverHost, port)
    jarPath = Path(os.path.join(TIKA_JAR_PATH, "tika-server.jar"))
    if "localhost" in server_endpoint or "127.0.0.1" in server_endpoint:
        alreadyRunning = check_port_is_open(remoteServerHost=serverHost, port=port)

        if not alreadyRunning:
            if not check_jar_signature(tikaServerJar=tikaServerJar, jarPath=jarPath):
                msg = f"Jar signature does not match for JAR {tikaServerJar} at path {jarPath}"
                log.error(msg)
                raise RuntimeError(msg)

            status = start_server(
                tikaServerJar=jarPath,
                java_path=TIKA_JAVA,
                java_args=TIKA_JAVA_ARGS,
                serverHost=serverHost,
                port=port,
                classpath=classpath,
                config_path=config_path,
            )
            if not status:
                log.error("Failed to receive startup confirmation from startServer.")
                raise RuntimeError("Unable to start Tika server.")
    return server_endpoint


def check_jar_signature(tikaServerJar, jarPath) -> bool:
    """
    Checks the signature of Jar
    :param tikaServerJar:
    :param jarPath:
    :return: ``True`` if the signature of the jar matches
    """
    if not os.path.isfile(jarPath + ".md5"):
        raise RuntimeError(f"MD5 file not found for JAR {tikaServerJar} at path {jarPath}")
    m = hashlib.md5()
    with open(jarPath, "rb") as f:
        binContents = f.read()
        m.update(binContents)
        with open(jarPath + ".md5", "r") as em:
            existingContents = em.read()
            return existingContents == m.hexdigest()


def start_server(
    tikaServerJar: Path,
    java_path: str = TIKA_JAVA,
    java_args: str = TIKA_JAVA_ARGS,
    serverHost: str = SERVER_HOST,
    port: str = PORT,
    classpath: str | None = None,
    config_path: str | None = None,
) -> bool:
    """
    Starts Tika Server
    :param tikaServerJar: path to tika server jar
    :param serverHost: the host interface address to be used for binding the service
    :param port: the host port to be used for binding the service
    :param classpath: Class path value to pass to JVM
    :return: None
    """
    if classpath is None:
        classpath = TIKA_SERVER_CLASSPATH

    host = "localhost"
    if IS_WINDOWS:
        host = "0.0.0.0"

    if classpath:
        if IS_WINDOWS:
            classpath += ";" + str(tikaServerJar)
            classpath = '"' + classpath + '"'
        else:
            classpath += ":" + str(tikaServerJar)
    else:
        classpath = str(tikaServerJar)

    # setup command string
    cmd_string = ""
    if not config_path:
        cmd_string = '%s %s -cp "%s" org.apache.tika.server.core.TikaServerCli --port %s --host %s &' % (
            java_path,
            java_args,
            classpath,
            port,
            host,
        )
    else:
        cmd_string = '%s %s -cp "%s" org.apache.tika.server.core.TikaServerCli --port %s --host %s --config %s &' % (
            java_path,
            java_args,
            classpath,
            port,
            host,
            config_path,
        )

    # Check that we can write to log path
    try:
        tika_log_file_path = os.path.join(TIKA_SERVER_LOG_FILE_PATH, "tika-server.log")
        logFile = open(tika_log_file_path, "w")
    except PermissionError:
        log.error("Unable to create tika-server.log at %s due to permission error." % (TIKA_SERVER_LOG_FILE_PATH))
        return False

    # Check that specified java binary is available on path
    try:
        _ = Popen(java_path, stdout=open(os.devnull, "w"), stderr=open(os.devnull, "w"))
    except FileNotFoundError:
        log.error("Unable to run java; is it installed?")
        return False

    # Run java with jar args
    global TIKA_SERVER_PROCESS
    # Patch for Windows support
    if IS_WINDOWS:
        if sys.version.startswith("2"):
            # Python 2.x
            TIKA_SERVER_PROCESS = Popen(cmd_string, stdout=logFile, stderr=STDOUT, shell=True)
        elif sys.version.startswith("3"):
            # Python 3.x
            TIKA_SERVER_PROCESS = Popen(cmd_string, stdout=logFile, stderr=STDOUT, shell=True, start_new_session=True)
    else:
        TIKA_SERVER_PROCESS = Popen(cmd_string, stdout=logFile, stderr=STDOUT, shell=True, preexec_fn=os.setsid)

    # Check logs and retry as configured
    try_count = 0
    is_started = False
    while try_count < TIKA_STARTUP_MAX_RETRY:
        with open(tika_log_file_path, "r") as tika_log_file_tmp:
            # check for INFO string to confirm listening endpoint
            if "Started Apache Tika server" in tika_log_file_tmp.read():
                is_started = True
                break
            else:
                log.warning("Failed to see startup log message; retrying...")
        time.sleep(TIKA_STARTUP_SLEEP)
        try_count += 1

    if not is_started:
        log.error("Tika startup log message not received after %d tries." % (TIKA_STARTUP_MAX_RETRY))
        return False
    else:
        return True


def kill_server(TikaServerProcess: Popen | None = None, Windows: bool = False) -> None:
    """
    Kills the tika server started by the current execution instance.

    Args:
        TikaServerProcess: The subprocess.Popen instance of the Tika server
        Windows: Boolean flag indicating if running on Windows platform
    """
    if TikaServerProcess is None:
        log.error("Server not running, or was already running before")
        return

    try:
        if Windows:
            if sys.version_info >= (3, 0):
                os.kill(TikaServerProcess.pid, signal.SIGTERM)
            else:
                # Legacy Python 2.x Windows support
                PROCESS_TERMINATE = 1
                handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE, False, TikaServerProcess.pid)
                ctypes.windll.kernel32.TerminateProcess(handle, -1)
                ctypes.windll.kernel32.CloseHandle(handle)
        else:
            os.killpg(os.getpgid(TikaServerProcess.pid), signal.SIGTERM)
    except (ProcessLookupError, OSError) as e:
        log.error("Failed to kill the current server session: %s", str(e))
    finally:
        time.sleep(1)


def to_filename(url) -> str:
    """
    Gets url and returns filename
    """
    urlp = urlparse(url)
    path = urlp.path
    if not path:
        path = "file_{}".format(int(time.time()))
    value = re.sub(r"[^\w\s\.\-]", "-", path).strip().lower()
    return re.sub(r"[-\s]+", "-", value).strip("-")[-200:]


def _is_file_object(f: Any) -> bool:
    try:
        file_types: tuple[type, ...] = (types.FileType, io.IOBase)  # type: ignore
    except AttributeError:
        file_types = (io.IOBase,)

    return isinstance(f, file_types)


def get_file_handle(urlOrPath: str | Path | BinaryIO) -> BinaryIO:
    """
    Opens a remote file and returns a file-like object.

    Args:
        urlOrPath: resource locator, generally URL or path, or file object

    Returns:
        file-like object
    """
    if isinstance(urlOrPath, Path):
        return open(urlOrPath, "rb")
    elif isinstance(urlOrPath, BinaryIO):
        return urlOrPath
    else:
        return open(urlOrPath, "rb")


def get_remote_file(
    urlOrPath: str | Path | BinaryIO,
    destPath: str | Path,
) -> tuple[Path, Literal["local", "remote", "binary"]]:
    """
    Fetches URL to local path or just returns absolute path.

    Args:
        urlOrPath: resource locator, generally URL or path, or file object
        destPath: path to store the resource, usually a path on file system

    Returns:
        tuple containing (path, source_type) where source_type is one of:
        'local', 'remote', or 'binary'
    """
    # handle binary stream input
    if isinstance(urlOrPath, Path):
        return (urlOrPath, "local")

    if isinstance(urlOrPath, io.IOBase | BinaryIO):
        if not hasattr(urlOrPath, "name"):
            name = "file_{}".format(int(time.time()))
        else:
            name = urlOrPath.name
        filename = to_filename(name)
        dest_path = Path(destPath) / filename
        with open(dest_path, "wb") as f:
            f.write(urlOrPath.read())
        return (dest_path, "binary")

    urlp = urlparse(urlOrPath)
    if urlp.scheme == "":
        path = Path(urlOrPath)
        if not path.exists():
            raise TikaException(f"File {path} does not exist.")
        return (path, "local")
    else:
        filename = to_filename(urlOrPath)  # Assuming to_filename exists and returns str
        dest_path = Path(destPath) / filename
        log.info("Retrieving %s to %s.", urlOrPath, dest_path)
        try:
            urlretrieve(urlOrPath, dest_path)
        except IOError:
            # monkey patch fix for SSL/Windows per Tika-Python #54
            # https://github.com/chrismattmann/tika-python/issues/54
            import ssl

            if hasattr(ssl, "_create_unverified_context"):
                ssl._create_default_https_context = ssl._create_unverified_context
            # delete whatever we had there
            if os.path.exists(dest_path) and os.path.isfile(dest_path):
                os.remove(dest_path)
            urlretrieve(urlOrPath, dest_path)
        return (dest_path, "remote")


def check_port_is_open(remoteServerHost=SERVER_HOST, port=PORT) -> bool:
    """
    Checks if the specified port is open
    :param remoteServerHost: the host address
    :param port: port which needs to be checked
    :return: ``True`` if port is open, ``False`` otherwise
    """
    remoteServerIP = socket.gethostbyname(remoteServerHost)

    sock: socket.socket | None = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remoteServerIP, int(port)))
        if result == 0:
            return True
        else:
            return False

    except KeyboardInterrupt:
        print("You pressed Ctrl+C")
        sys.exit()

    except socket.gaierror:
        print("Hostname could not be resolved. Exiting")
        sys.exit()

    except socket.error:
        print("Couldn't connect to server")
        sys.exit()

    finally:
        if sock:
            sock.close()


def main(argv=None):
    """Run Tika from command line according to USAGE."""
    global VERBOSE
    global ENCODE_UTF8
    global CSV_OUTPUT
    if argv is None:
        argv = sys.argv

    if len(argv) < 3 and not (("-h" in argv) or ("--help" in argv)):
        log.exception("Bad args")
        raise TikaException("Bad args")
    try:
        opts, argv = getopt.getopt(
            argv[1:], "hi:s:o:p:v:e:c", ["help", "install=", "server=", "output=", "port=", "verbose", "encode", "csv"]
        )
    except getopt.GetoptError as opt_error:
        msg, bad_opt = opt_error  # type: ignore
        log.exception("%s error: Bad option: %s, %s" % (argv[0], bad_opt, msg))
        raise TikaException("%s error: Bad option: %s, %s" % (argv[0], bad_opt, msg))

    tikaServerJar = TikaServerJar
    serverHost = SERVER_HOST
    outDir = Path(".")
    port = PORT
    for opt, val in opts:
        if opt in ("-h", "--help"):
            echo2(USAGE)
            sys.exit()
        elif opt in ("--install"):
            tikaServerJar = Path(val)
        elif opt in ("--server"):
            serverHost = val
        elif opt in ("-o", "--output"):
            outDir = Path(val)
        elif opt in ("--port"):
            port = val
        elif opt in ("-v", "--verbose"):
            VERBOSE = 1
        elif opt in ("-e", "--encode"):
            ENCODE_UTF8 = 1
        elif opt in ("-c", "--csv"):
            CSV_OUTPUT = 1
        else:
            raise TikaException(USAGE)

    cmd = argv[0]
    option = argv[1]
    try:
        paths = argv[2:]
    except:  # noqa: E722
        paths = None
    return run_command(
        cmd=cmd,
        option=option,
        urlOrPaths=paths,
        port=port,
        outDir=outDir,
        serverHost=serverHost,
        tikaServerJar=tikaServerJar,
        verbose=VERBOSE,
        encode=ENCODE_UTF8,
    )


if __name__ == "__main__":
    log.info("Logging on '%s'" % (LOG_FILE))
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
        raise TikaException("Unsupported Python version")

    if type(resp) is list:
        out.write("\n".join([r[1] for r in resp]))  # type: ignore
    elif type(resp) is str:
        out.write(resp)
    else:
        raise TikaException("Bad response type")
    out.write("\n")
