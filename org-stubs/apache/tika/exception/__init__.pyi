
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import org.xml.sax
import typing



class FileTooLongException(java.io.IOException):
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def __init__(self, long: int, long2: int): ...

class RuntimeSAXException(java.lang.RuntimeException):
    def __init__(self, sAXException: org.xml.sax.SAXException): ...

class TikaException(java.lang.Exception):
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def __init__(self, string: str, throwable: java.lang.Throwable): ...

class TikaTimeoutException(java.lang.RuntimeException):
    def __init__(self, string: str): ...

class WriteLimitReachedException(org.xml.sax.SAXException):
    def __init__(self, int: int): ...
    def getMessage(self) -> str: ...
    @staticmethod
    def isWriteLimitReached(throwable: java.lang.Throwable) -> bool: ...
    @staticmethod
    def throwIfWriteLimitReached(exception: java.lang.Exception) -> None: ...

class AccessPermissionException(TikaException):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def __init__(self, string: str, throwable: java.lang.Throwable): ...
    @typing.overload
    def __init__(self, throwable: java.lang.Throwable): ...

class CorruptedFileException(TikaException):
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def __init__(self, string: str, throwable: java.lang.Throwable): ...

class EncryptedDocumentException(TikaException):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def __init__(self, string: str, throwable: java.lang.Throwable): ...
    @typing.overload
    def __init__(self, throwable: java.lang.Throwable): ...

class TikaConfigException(TikaException):
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def __init__(self, string: str, throwable: java.lang.Throwable): ...

class TikaMemoryLimitException(TikaException):
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def __init__(self, long: int, long2: int): ...

class UnsupportedFormatException(TikaException):
    def __init__(self, string: str): ...

class ZeroByteFileException(TikaException):
    IGNORE_ZERO_BYTE_FILE_EXCEPTION: typing.ClassVar['ZeroByteFileException.IgnoreZeroByteFileException'] = ...
    def __init__(self, string: str): ...
    class IgnoreZeroByteFileException:
        def __init__(self): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.exception")``.

    AccessPermissionException: typing.Type[AccessPermissionException]
    CorruptedFileException: typing.Type[CorruptedFileException]
    EncryptedDocumentException: typing.Type[EncryptedDocumentException]
    FileTooLongException: typing.Type[FileTooLongException]
    RuntimeSAXException: typing.Type[RuntimeSAXException]
    TikaConfigException: typing.Type[TikaConfigException]
    TikaException: typing.Type[TikaException]
    TikaMemoryLimitException: typing.Type[TikaMemoryLimitException]
    TikaTimeoutException: typing.Type[TikaTimeoutException]
    UnsupportedFormatException: typing.Type[UnsupportedFormatException]
    WriteLimitReachedException: typing.Type[WriteLimitReachedException]
    ZeroByteFileException: typing.Type[ZeroByteFileException]
