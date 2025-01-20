
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.nio.file
import java.util
import jpype.protocol
import org.apache.tika.config
import org.apache.tika.pipes.pipesiterator
import typing



class FileSystemPipesIterator(org.apache.tika.pipes.pipesiterator.PipesIterator, org.apache.tika.pipes.pipesiterator.TotalCounter, org.apache.tika.config.Initializable, java.io.Closeable):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath]): ...
    def checkInitialization(self, initializableProblemHandler: typing.Union[org.apache.tika.config.InitializableProblemHandler, typing.Callable]) -> None: ...
    def close(self) -> None: ...
    def getTotalCount(self) -> org.apache.tika.pipes.pipesiterator.TotalCountResult: ...
    def initialize(self, map: typing.Union[java.util.Map[str, org.apache.tika.config.Param], typing.Mapping[str, org.apache.tika.config.Param]]) -> None: ...
    def setBasePath(self, string: str) -> None: ...
    def setCountTotal(self, boolean: bool) -> None: ...
    def startTotalCount(self) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.pipes.pipesiterator.fs")``.

    FileSystemPipesIterator: typing.Type[FileSystemPipesIterator]
