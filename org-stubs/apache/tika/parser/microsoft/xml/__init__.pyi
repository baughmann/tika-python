
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



class AbstractXML2003Parser(org.apache.tika.parser.Parser):
    def __init__(self): ...
    def parse(self, inputStream: java.io.InputStream, contentHandler: org.xml.sax.ContentHandler, metadata: org.apache.tika.metadata.Metadata, parseContext: org.apache.tika.parser.ParseContext) -> None: ...

class SpreadsheetMLParser(AbstractXML2003Parser):
    def __init__(self): ...
    def getSupportedTypes(self, parseContext: org.apache.tika.parser.ParseContext) -> java.util.Set[org.apache.tika.mime.MediaType]: ...
    def setContentType(self, metadata: org.apache.tika.metadata.Metadata) -> None: ...

class WordMLParser(AbstractXML2003Parser):
    def __init__(self): ...
    def getSupportedTypes(self, parseContext: org.apache.tika.parser.ParseContext) -> java.util.Set[org.apache.tika.mime.MediaType]: ...
    def setContentType(self, metadata: org.apache.tika.metadata.Metadata) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.parser.microsoft.xml")``.

    AbstractXML2003Parser: typing.Type[AbstractXML2003Parser]
    SpreadsheetMLParser: typing.Type[SpreadsheetMLParser]
    WordMLParser: typing.Type[WordMLParser]
