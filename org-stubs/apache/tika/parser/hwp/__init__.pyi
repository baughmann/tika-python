
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.security
import java.util
import org.apache.tika.metadata
import org.apache.tika.mime
import org.apache.tika.parser
import org.apache.tika.sax
import org.xml.sax
import typing



class HwpStreamReader:
    def __init__(self, inputStream: java.io.InputStream): ...
    def skipFully(self, long: int) -> None: ...
    @typing.overload
    def uint16(self) -> int: ...
    @typing.overload
    def uint16(self, int: int) -> typing.MutableSequence[int]: ...
    def uint32(self) -> int: ...
    def uint8(self) -> int: ...

class HwpTextExtractorV5(java.io.Serializable):
    def __init__(self): ...
    def createDecryptStream(self, inputStream: java.io.InputStream, key: java.security.Key) -> java.io.InputStream: ...
    def extract(self, inputStream: java.io.InputStream, metadata: org.apache.tika.metadata.Metadata, xHTMLContentHandler: org.apache.tika.sax.XHTMLContentHandler) -> None: ...

class HwpV5Parser(org.apache.tika.parser.Parser):
    HWP_MIME_TYPE: typing.ClassVar[str] = ...
    def __init__(self): ...
    def getSupportedTypes(self, parseContext: org.apache.tika.parser.ParseContext) -> java.util.Set[org.apache.tika.mime.MediaType]: ...
    def parse(self, inputStream: java.io.InputStream, contentHandler: org.xml.sax.ContentHandler, metadata: org.apache.tika.metadata.Metadata, parseContext: org.apache.tika.parser.ParseContext) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.parser.hwp")``.

    HwpStreamReader: typing.Type[HwpStreamReader]
    HwpTextExtractorV5: typing.Type[HwpTextExtractorV5]
    HwpV5Parser: typing.Type[HwpV5Parser]
