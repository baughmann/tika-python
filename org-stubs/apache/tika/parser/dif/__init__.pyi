
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.util
import jpype
import org.apache.tika.metadata
import org.apache.tika.mime
import org.apache.tika.parser
import org.xml.sax
import org.xml.sax.helpers
import typing



class DIFContentHandler(org.xml.sax.helpers.DefaultHandler):
    def __init__(self, contentHandler: org.xml.sax.ContentHandler, metadata: org.apache.tika.metadata.Metadata): ...
    def characters(self, charArray: typing.Union[typing.List[str], jpype.JArray], int: int, int2: int) -> None: ...
    def endDocument(self) -> None: ...
    def endElement(self, string: str, string2: str, string3: str) -> None: ...
    def ignorableWhitespace(self, charArray: typing.Union[typing.List[str], jpype.JArray], int: int, int2: int) -> None: ...
    def setDocumentLocator(self, locator: org.xml.sax.Locator) -> None: ...
    def startDocument(self) -> None: ...
    def startElement(self, string: str, string2: str, string3: str, attributes: org.xml.sax.Attributes) -> None: ...
    def toString(self) -> str: ...

class DIFParser(org.apache.tika.parser.Parser):
    def __init__(self): ...
    def getSupportedTypes(self, parseContext: org.apache.tika.parser.ParseContext) -> java.util.Set[org.apache.tika.mime.MediaType]: ...
    def parse(self, inputStream: java.io.InputStream, contentHandler: org.xml.sax.ContentHandler, metadata: org.apache.tika.metadata.Metadata, parseContext: org.apache.tika.parser.ParseContext) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.parser.dif")``.

    DIFContentHandler: typing.Type[DIFContentHandler]
    DIFParser: typing.Type[DIFParser]
