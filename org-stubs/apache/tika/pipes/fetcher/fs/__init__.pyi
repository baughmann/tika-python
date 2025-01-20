
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.nio.file
import java.util
import org.apache.tika.config
import org.apache.tika.metadata
import org.apache.tika.parser
import org.apache.tika.pipes.fetcher
import org.apache.tika.pipes.fetcher.fs.config
import typing



class FileSystemFetcher(org.apache.tika.pipes.fetcher.AbstractFetcher, org.apache.tika.config.Initializable):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, fileSystemFetcherConfig: org.apache.tika.pipes.fetcher.fs.config.FileSystemFetcherConfig): ...
    def checkInitialization(self, initializableProblemHandler: typing.Union[org.apache.tika.config.InitializableProblemHandler, typing.Callable]) -> None: ...
    def fetch(self, string: str, metadata: org.apache.tika.metadata.Metadata, parseContext: org.apache.tika.parser.ParseContext) -> java.io.InputStream: ...
    def getBasePath(self) -> java.nio.file.Path: ...
    def initialize(self, map: typing.Union[java.util.Map[str, org.apache.tika.config.Param], typing.Mapping[str, org.apache.tika.config.Param]]) -> None: ...
    def setBasePath(self, string: str) -> None: ...
    def setExtractFileSystemMetadata(self, boolean: bool) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.pipes.fetcher.fs")``.

    FileSystemFetcher: typing.Type[FileSystemFetcher]
    config: org.apache.tika.pipes.fetcher.fs.config.__module_protocol__
