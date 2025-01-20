
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.net
import java.nio.channels
import java.nio.file
import java.sql
import jpype
import jpype.protocol
import org.apache.commons.io.input
import org.apache.tika.exception
import org.apache.tika.metadata
import typing



class BoundedInputStream(java.io.InputStream):
    def __init__(self, long: int, inputStream: java.io.InputStream): ...
    def available(self) -> int: ...
    def getPos(self) -> int: ...
    def hasHitBound(self) -> bool: ...
    def mark(self, int: int) -> None: ...
    def markSupported(self) -> bool: ...
    @typing.overload
    def read(self) -> int: ...
    @typing.overload
    def read(self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> int: ...
    @typing.overload
    def read(self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], int: int, int2: int) -> int: ...
    @typing.overload
    def readNBytes(self, int: int) -> typing.MutableSequence[int]: ...
    @typing.overload
    def readNBytes(self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], int: int, int2: int) -> int: ...
    def reset(self) -> None: ...
    def skip(self, long: int) -> int: ...
    def transferTo(self, outputStream: java.io.OutputStream) -> int: ...

class EndianUtils:
    def __init__(self): ...
    @typing.overload
    @staticmethod
    def getIntBE(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> int: ...
    @typing.overload
    @staticmethod
    def getIntBE(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], int: int) -> int: ...
    @typing.overload
    @staticmethod
    def getIntLE(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> int: ...
    @typing.overload
    @staticmethod
    def getIntLE(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], int: int) -> int: ...
    @staticmethod
    def getLongLE(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], int: int) -> int: ...
    @typing.overload
    @staticmethod
    def getShortBE(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> int: ...
    @typing.overload
    @staticmethod
    def getShortBE(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], int: int) -> int: ...
    @typing.overload
    @staticmethod
    def getShortLE(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> int: ...
    @typing.overload
    @staticmethod
    def getShortLE(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], int: int) -> int: ...
    @staticmethod
    def getUByte(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], int: int) -> int: ...
    @typing.overload
    @staticmethod
    def getUIntBE(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> int: ...
    @typing.overload
    @staticmethod
    def getUIntBE(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], int: int) -> int: ...
    @typing.overload
    @staticmethod
    def getUIntLE(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> int: ...
    @typing.overload
    @staticmethod
    def getUIntLE(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], int: int) -> int: ...
    @typing.overload
    @staticmethod
    def getUShortBE(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> int: ...
    @typing.overload
    @staticmethod
    def getUShortBE(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], int: int) -> int: ...
    @typing.overload
    @staticmethod
    def getUShortLE(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> int: ...
    @typing.overload
    @staticmethod
    def getUShortLE(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], int: int) -> int: ...
    @staticmethod
    def readIntBE(inputStream: java.io.InputStream) -> int: ...
    @staticmethod
    def readIntLE(inputStream: java.io.InputStream) -> int: ...
    @staticmethod
    def readIntME(inputStream: java.io.InputStream) -> int: ...
    @staticmethod
    def readLongBE(inputStream: java.io.InputStream) -> int: ...
    @staticmethod
    def readLongLE(inputStream: java.io.InputStream) -> int: ...
    @staticmethod
    def readShortBE(inputStream: java.io.InputStream) -> int: ...
    @staticmethod
    def readShortLE(inputStream: java.io.InputStream) -> int: ...
    @staticmethod
    def readUE7(inputStream: java.io.InputStream) -> int: ...
    @staticmethod
    def readUIntBE(inputStream: java.io.InputStream) -> int: ...
    @staticmethod
    def readUIntLE(inputStream: java.io.InputStream) -> int: ...
    @staticmethod
    def readUShortBE(inputStream: java.io.InputStream) -> int: ...
    @staticmethod
    def readUShortLE(inputStream: java.io.InputStream) -> int: ...
    @staticmethod
    def ubyteToInt(byte: int) -> int: ...
    class BufferUnderrunException(org.apache.tika.exception.TikaException):
        def __init__(self): ...

class FilenameUtils:
    RESERVED_FILENAME_CHARACTERS: typing.ClassVar[typing.MutableSequence[str]] = ...
    def __init__(self): ...
    @staticmethod
    def getName(string: str) -> str: ...
    @staticmethod
    def getSuffixFromPath(string: str) -> str: ...
    @staticmethod
    def normalize(string: str) -> str: ...

class IOUtils:
    def __init__(self): ...
    @staticmethod
    def skip(inputStream: java.io.InputStream, long: int, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> int: ...

class InputStreamFactory:
    def getInputStream(self) -> java.io.InputStream: ...

class LookaheadInputStream(java.io.InputStream):
    def __init__(self, inputStream: java.io.InputStream, int: int): ...
    def available(self) -> int: ...
    def close(self) -> None: ...
    def mark(self, int: int) -> None: ...
    def markSupported(self) -> bool: ...
    @typing.overload
    def read(self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> int: ...
    @typing.overload
    def read(self) -> int: ...
    @typing.overload
    def read(self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], int: int, int2: int) -> int: ...
    def reset(self) -> None: ...
    def skip(self, long: int) -> int: ...

class TailStream(java.io.FilterInputStream):
    def __init__(self, inputStream: java.io.InputStream, int: int): ...
    def getTail(self) -> typing.MutableSequence[int]: ...
    def mark(self, int: int) -> None: ...
    @typing.overload
    def read(self) -> int: ...
    @typing.overload
    def read(self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> int: ...
    @typing.overload
    def read(self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], int: int, int2: int) -> int: ...
    def reset(self) -> None: ...
    def skip(self, long: int) -> int: ...

class TemporaryResources(java.io.Closeable):
    def __init__(self): ...
    def addResource(self, closeable: typing.Union[java.io.Closeable, typing.Callable]) -> None: ...
    def close(self) -> None: ...
    @typing.overload
    def createTempFile(self) -> java.nio.file.Path: ...
    @typing.overload
    def createTempFile(self, string: str) -> java.nio.file.Path: ...
    @typing.overload
    def createTempFile(self, metadata: org.apache.tika.metadata.Metadata) -> java.nio.file.Path: ...
    def createTemporaryFile(self) -> java.io.File: ...
    def dispose(self) -> None: ...
    _getResource__T = typing.TypeVar('_getResource__T', bound=java.io.Closeable)  # <T>
    def getResource(self, class_: typing.Type[_getResource__T]) -> _getResource__T: ...
    @typing.overload
    def setTemporaryFileDirectory(self, file: typing.Union[java.io.File, jpype.protocol.SupportsPath]) -> None: ...
    @typing.overload
    def setTemporaryFileDirectory(self, path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath]) -> None: ...

class TikaInputStream(org.apache.commons.io.input.TaggedInputStream):
    def addCloseableResource(self, closeable: typing.Union[java.io.Closeable, typing.Callable]) -> None: ...
    @staticmethod
    def cast(inputStream: java.io.InputStream) -> 'TikaInputStream': ...
    def close(self) -> None: ...
    @typing.overload
    @staticmethod
    def get(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> 'TikaInputStream': ...
    @typing.overload
    @staticmethod
    def get(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], metadata: org.apache.tika.metadata.Metadata) -> 'TikaInputStream': ...
    @typing.overload
    @staticmethod
    def get(file: typing.Union[java.io.File, jpype.protocol.SupportsPath]) -> 'TikaInputStream': ...
    @typing.overload
    @staticmethod
    def get(file: typing.Union[java.io.File, jpype.protocol.SupportsPath], metadata: org.apache.tika.metadata.Metadata) -> 'TikaInputStream': ...
    @typing.overload
    @staticmethod
    def get(inputStream: java.io.InputStream) -> 'TikaInputStream': ...
    @typing.overload
    @staticmethod
    def get(inputStream: java.io.InputStream, temporaryResources: TemporaryResources, metadata: org.apache.tika.metadata.Metadata) -> 'TikaInputStream': ...
    @typing.overload
    @staticmethod
    def get(uRI: java.net.URI) -> 'TikaInputStream': ...
    @typing.overload
    @staticmethod
    def get(uRI: java.net.URI, metadata: org.apache.tika.metadata.Metadata) -> 'TikaInputStream': ...
    @typing.overload
    @staticmethod
    def get(uRL: java.net.URL) -> 'TikaInputStream': ...
    @typing.overload
    @staticmethod
    def get(uRL: java.net.URL, metadata: org.apache.tika.metadata.Metadata) -> 'TikaInputStream': ...
    @typing.overload
    @staticmethod
    def get(path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath]) -> 'TikaInputStream': ...
    @typing.overload
    @staticmethod
    def get(path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath], metadata: org.apache.tika.metadata.Metadata) -> 'TikaInputStream': ...
    @typing.overload
    @staticmethod
    def get(path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath], metadata: org.apache.tika.metadata.Metadata, temporaryResources: TemporaryResources) -> 'TikaInputStream': ...
    @typing.overload
    @staticmethod
    def get(blob: java.sql.Blob) -> 'TikaInputStream': ...
    @typing.overload
    @staticmethod
    def get(blob: java.sql.Blob, metadata: org.apache.tika.metadata.Metadata) -> 'TikaInputStream': ...
    @typing.overload
    @staticmethod
    def get(inputStreamFactory: typing.Union[InputStreamFactory, typing.Callable]) -> 'TikaInputStream': ...
    @typing.overload
    @staticmethod
    def get(inputStreamFactory: typing.Union[InputStreamFactory, typing.Callable], temporaryResources: TemporaryResources) -> 'TikaInputStream': ...
    def getFile(self) -> java.io.File: ...
    def getFileChannel(self) -> java.nio.channels.FileChannel: ...
    def getInputStreamFactory(self) -> InputStreamFactory: ...
    def getLength(self) -> int: ...
    def getOpenContainer(self) -> typing.Any: ...
    @typing.overload
    def getPath(self) -> java.nio.file.Path: ...
    @typing.overload
    def getPath(self, int: int) -> java.nio.file.Path: ...
    def getPosition(self) -> int: ...
    def hasFile(self) -> bool: ...
    def hasInputStreamFactory(self) -> bool: ...
    def hasLength(self) -> bool: ...
    @staticmethod
    def isTikaInputStream(inputStream: java.io.InputStream) -> bool: ...
    def mark(self, int: int) -> None: ...
    def markSupported(self) -> bool: ...
    def peek(self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> int: ...
    def reset(self) -> None: ...
    def setOpenContainer(self, object: typing.Any) -> None: ...
    def skip(self, long: int) -> int: ...
    def toString(self) -> str: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.io")``.

    BoundedInputStream: typing.Type[BoundedInputStream]
    EndianUtils: typing.Type[EndianUtils]
    FilenameUtils: typing.Type[FilenameUtils]
    IOUtils: typing.Type[IOUtils]
    InputStreamFactory: typing.Type[InputStreamFactory]
    LookaheadInputStream: typing.Type[LookaheadInputStream]
    TailStream: typing.Type[TailStream]
    TemporaryResources: typing.Type[TemporaryResources]
    TikaInputStream: typing.Type[TikaInputStream]
