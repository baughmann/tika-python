
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.nio.file
import java.util
import jpype.protocol
import org.apache.pdfbox.io
import typing



class IncrementalUpdateRecord:
    def __init__(self, path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath], list: java.util.List['StartXRefOffset']): ...
    def getOffsets(self) -> java.util.List['StartXRefOffset']: ...
    def getPath(self) -> java.nio.file.Path: ...

class IsIncrementalUpdate:
    IS_INCREMENTAL_UPDATE: typing.ClassVar['IsIncrementalUpdate'] = ...
    def __init__(self): ...

class StartXRefOffset:
    def __init__(self, long: int, long2: int, long3: int, boolean: bool): ...
    def getEndEofOffset(self) -> int: ...
    def getStartXrefOffset(self) -> int: ...
    def getStartxref(self) -> int: ...
    def isHasEof(self) -> bool: ...
    def toString(self) -> str: ...

class StartXRefScanner:
    def __init__(self, randomAccessRead: org.apache.pdfbox.io.RandomAccessRead): ...
    def scan(self) -> java.util.List[StartXRefOffset]: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.parser.pdf.updates")``.

    IncrementalUpdateRecord: typing.Type[IncrementalUpdateRecord]
    IsIncrementalUpdate: typing.Type[IsIncrementalUpdate]
    StartXRefOffset: typing.Type[StartXRefOffset]
    StartXRefScanner: typing.Type[StartXRefScanner]
