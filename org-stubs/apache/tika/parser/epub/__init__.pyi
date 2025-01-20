
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
import org.apache.tika.parser.xml
import org.xml.sax
import typing



class EpubContentParser(org.apache.tika.parser.Parser):
    def __init__(self): ...
    def getSupportedTypes(self, parseContext: org.apache.tika.parser.ParseContext) -> java.util.Set[org.apache.tika.mime.MediaType]: ...
    def parse(self, inputStream: java.io.InputStream, contentHandler: org.xml.sax.ContentHandler, metadata: org.apache.tika.metadata.Metadata, parseContext: org.apache.tika.parser.ParseContext) -> None: ...

class EpubParser(org.apache.tika.parser.Parser):
    def __init__(self): ...
    def getContentParser(self) -> org.apache.tika.parser.Parser: ...
    def getMetaParser(self) -> org.apache.tika.parser.Parser: ...
    def getSupportedTypes(self, parseContext: org.apache.tika.parser.ParseContext) -> java.util.Set[org.apache.tika.mime.MediaType]: ...
    def parse(self, inputStream: java.io.InputStream, contentHandler: org.xml.sax.ContentHandler, metadata: org.apache.tika.metadata.Metadata, parseContext: org.apache.tika.parser.ParseContext) -> None: ...
    def setContentParser(self, parser: org.apache.tika.parser.Parser) -> None: ...
    def setMetaParser(self, parser: org.apache.tika.parser.Parser) -> None: ...
    def setStreaming(self, boolean: bool) -> None: ...

class OPFParser(org.apache.tika.parser.xml.DcXMLParser):
    def __init__(self): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.parser.epub")``.

    EpubContentParser: typing.Type[EpubContentParser]
    EpubParser: typing.Type[EpubParser]
    OPFParser: typing.Type[OPFParser]
