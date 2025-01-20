
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
import org.apache.tika.sax
import org.xml.sax
import typing



class ExecutableParser(org.apache.tika.parser.Parser, org.apache.tika.metadata.MachineMetadata):
    def __init__(self): ...
    def getSupportedTypes(self, parseContext: org.apache.tika.parser.ParseContext) -> java.util.Set[org.apache.tika.mime.MediaType]: ...
    def parse(self, inputStream: java.io.InputStream, contentHandler: org.xml.sax.ContentHandler, metadata: org.apache.tika.metadata.Metadata, parseContext: org.apache.tika.parser.ParseContext) -> None: ...
    def parseELF(self, xHTMLContentHandler: org.apache.tika.sax.XHTMLContentHandler, metadata: org.apache.tika.metadata.Metadata, inputStream: java.io.InputStream, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> None: ...
    def parseMachO(self, xHTMLContentHandler: org.apache.tika.sax.XHTMLContentHandler, metadata: org.apache.tika.metadata.Metadata, inputStream: java.io.InputStream, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> None: ...
    def parsePE(self, xHTMLContentHandler: org.apache.tika.sax.XHTMLContentHandler, metadata: org.apache.tika.metadata.Metadata, inputStream: java.io.InputStream, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.parser.executable")``.

    ExecutableParser: typing.Type[ExecutableParser]
