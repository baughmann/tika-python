
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import org.apache.tika.config
import org.apache.tika.pipes.pipesiterator
import typing



class FileListPipesIterator(org.apache.tika.pipes.pipesiterator.PipesIterator, org.apache.tika.config.Initializable):
    def __init__(self): ...
    def checkInitialization(self, initializableProblemHandler: typing.Union[org.apache.tika.config.InitializableProblemHandler, typing.Callable]) -> None: ...
    def setFileList(self, string: str) -> None: ...
    def setHasHeader(self, boolean: bool) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.pipes.pipesiterator.filelist")``.

    FileListPipesIterator: typing.Type[FileListPipesIterator]
