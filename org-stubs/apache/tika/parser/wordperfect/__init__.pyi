
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



class QuattroProParser(org.apache.tika.parser.Parser):
    QP_9: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    QP_7_8: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    def __init__(self): ...
    def getSupportedTypes(self, parseContext: org.apache.tika.parser.ParseContext) -> java.util.Set[org.apache.tika.mime.MediaType]: ...
    def parse(self, inputStream: java.io.InputStream, contentHandler: org.xml.sax.ContentHandler, metadata: org.apache.tika.metadata.Metadata, parseContext: org.apache.tika.parser.ParseContext) -> None: ...

class WordPerfectParser(org.apache.tika.parser.Parser):
    def __init__(self): ...
    def getSupportedTypes(self, parseContext: org.apache.tika.parser.ParseContext) -> java.util.Set[org.apache.tika.mime.MediaType]: ...
    def isIncludeDeletedContent(self) -> bool: ...
    def parse(self, inputStream: java.io.InputStream, contentHandler: org.xml.sax.ContentHandler, metadata: org.apache.tika.metadata.Metadata, parseContext: org.apache.tika.parser.ParseContext) -> None: ...
    def setIncludeDeletedContent(self, boolean: bool) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.parser.wordperfect")``.

    QuattroProParser: typing.Type[QuattroProParser]
    WordPerfectParser: typing.Type[WordPerfectParser]
