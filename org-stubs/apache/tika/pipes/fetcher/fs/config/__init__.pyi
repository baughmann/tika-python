
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import org.apache.tika.pipes.fetcher.config
import typing



class FileSystemFetcherConfig(org.apache.tika.pipes.fetcher.config.AbstractConfig):
    def __init__(self): ...
    def getBasePath(self) -> str: ...
    def isExtractFileSystemMetadata(self) -> bool: ...
    def setBasePath(self, string: str) -> 'FileSystemFetcherConfig': ...
    def setExtractFileSystemMetadata(self, boolean: bool) -> 'FileSystemFetcherConfig': ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.pipes.fetcher.fs.config")``.

    FileSystemFetcherConfig: typing.Type[FileSystemFetcherConfig]
