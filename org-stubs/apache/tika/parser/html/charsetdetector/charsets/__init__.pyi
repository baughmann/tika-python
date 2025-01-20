
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import java.nio.charset
import typing



class ReplacementCharset(java.nio.charset.Charset):
    def __init__(self): ...
    def contains(self, charset: java.nio.charset.Charset) -> bool: ...
    def newDecoder(self) -> java.nio.charset.CharsetDecoder: ...
    def newEncoder(self) -> java.nio.charset.CharsetEncoder: ...

class XUserDefinedCharset(java.nio.charset.Charset):
    def __init__(self): ...
    def contains(self, charset: java.nio.charset.Charset) -> bool: ...
    def newDecoder(self) -> java.nio.charset.CharsetDecoder: ...
    def newEncoder(self) -> java.nio.charset.CharsetEncoder: ...
    class NotImplementedException(java.lang.RuntimeException):
        def __init__(self, string: str): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.parser.html.charsetdetector.charsets")``.

    ReplacementCharset: typing.Type[ReplacementCharset]
    XUserDefinedCharset: typing.Type[XUserDefinedCharset]
