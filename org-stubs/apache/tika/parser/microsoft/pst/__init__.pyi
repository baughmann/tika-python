
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.util
import org.apache.tika.metadata
import org.apache.tika.mime
import org.apache.tika.parser
import org.xml.sax
import typing



class OutlookPSTParser(org.apache.tika.parser.Parser):
    MS_OUTLOOK_PST_MIMETYPE: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    def __init__(self): ...
    def getSupportedTypes(self, parseContext: org.apache.tika.parser.ParseContext) -> java.util.Set[org.apache.tika.mime.MediaType]: ...
    def parse(self, inputStream: java.io.InputStream, contentHandler: org.xml.sax.ContentHandler, metadata: org.apache.tika.metadata.Metadata, parseContext: org.apache.tika.parser.ParseContext) -> None: ...

class PSTMailItemParser(org.apache.tika.parser.Parser):
    PST_MAIL_ITEM: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    PST_MAIL_ITEM_STRING: typing.ClassVar[str] = ...
    SUPPORTED_ITEMS: typing.ClassVar[java.util.Set] = ...
    def __init__(self): ...
    def getSupportedTypes(self, parseContext: org.apache.tika.parser.ParseContext) -> java.util.Set[org.apache.tika.mime.MediaType]: ...
    def parse(self, inputStream: java.io.InputStream, contentHandler: org.xml.sax.ContentHandler, metadata: org.apache.tika.metadata.Metadata, parseContext: org.apache.tika.parser.ParseContext) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.parser.microsoft.pst")``.

    OutlookPSTParser: typing.Type[OutlookPSTParser]
    PSTMailItemParser: typing.Type[PSTMailItemParser]
