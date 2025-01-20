
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import java.util
import jpype
import org.apache.tika.parser.microsoft.onenote.fsshttpb.streamobj
import typing



class AbstractChunking:
    def chunking(self) -> java.util.List[org.apache.tika.parser.microsoft.onenote.fsshttpb.streamobj.LeafNodeObject]: ...

class ChunkingFactory:
    @typing.overload
    @staticmethod
    def createChunkingInstance(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> AbstractChunking: ...
    @typing.overload
    @staticmethod
    def createChunkingInstance(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], chunkingMethod: 'ChunkingMethod') -> AbstractChunking: ...
    @typing.overload
    @staticmethod
    def createChunkingInstance(intermediateNodeObject: org.apache.tika.parser.microsoft.onenote.fsshttpb.streamobj.IntermediateNodeObject) -> AbstractChunking: ...

class ChunkingMethod(java.lang.Enum['ChunkingMethod']):
    ZipAlgorithm: typing.ClassVar['ChunkingMethod'] = ...
    RDCAnalysis: typing.ClassVar['ChunkingMethod'] = ...
    SimpleAlgorithm: typing.ClassVar['ChunkingMethod'] = ...
    _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'ChunkingMethod': ...
    @staticmethod
    def values() -> typing.MutableSequence['ChunkingMethod']: ...

class RDCAnalysisChunking(AbstractChunking):
    def __init__(self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]): ...
    def chunking(self) -> java.util.List[org.apache.tika.parser.microsoft.onenote.fsshttpb.streamobj.LeafNodeObject]: ...

class SimpleChunking(AbstractChunking):
    def __init__(self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]): ...
    def chunking(self) -> java.util.List[org.apache.tika.parser.microsoft.onenote.fsshttpb.streamobj.LeafNodeObject]: ...

class ZipFilesChunking(AbstractChunking):
    def __init__(self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]): ...
    def chunking(self) -> java.util.List[org.apache.tika.parser.microsoft.onenote.fsshttpb.streamobj.LeafNodeObject]: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.parser.microsoft.onenote.fsshttpb.streamobj.chunking")``.

    AbstractChunking: typing.Type[AbstractChunking]
    ChunkingFactory: typing.Type[ChunkingFactory]
    ChunkingMethod: typing.Type[ChunkingMethod]
    RDCAnalysisChunking: typing.Type[RDCAnalysisChunking]
    SimpleChunking: typing.Type[SimpleChunking]
    ZipFilesChunking: typing.Type[ZipFilesChunking]
