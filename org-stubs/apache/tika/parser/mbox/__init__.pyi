
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



class MboxParser(org.apache.tika.parser.Parser):
    MBOX_MIME_TYPE: typing.ClassVar[str] = ...
    MBOX_RECORD_DIVIDER: typing.ClassVar[str] = ...
    MAIL_MAX_SIZE: typing.ClassVar[int] = ...
    def __init__(self): ...
    def getSupportedTypes(self, parseContext: org.apache.tika.parser.ParseContext) -> java.util.Set[org.apache.tika.mime.MediaType]: ...
    def getTrackingMetadata(self) -> java.util.Map[int, org.apache.tika.metadata.Metadata]: ...
    def isTracking(self) -> bool: ...
    def parse(self, inputStream: java.io.InputStream, contentHandler: org.xml.sax.ContentHandler, metadata: org.apache.tika.metadata.Metadata, parseContext: org.apache.tika.parser.ParseContext) -> None: ...
    def setTracking(self, boolean: bool) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.parser.mbox")``.

    MboxParser: typing.Type[MboxParser]
