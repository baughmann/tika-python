
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.util
import org.apache.tika.detect
import org.apache.tika.metadata
import org.apache.tika.mime
import org.apache.tika.parser
import org.xml.sax
import typing



class SourceCodeParser(org.apache.tika.parser.AbstractEncodingDetectorParser):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, encodingDetector: typing.Union[org.apache.tika.detect.EncodingDetector, typing.Callable]): ...
    def getSupportedTypes(self, parseContext: org.apache.tika.parser.ParseContext) -> java.util.Set[org.apache.tika.mime.MediaType]: ...
    def parse(self, inputStream: java.io.InputStream, contentHandler: org.xml.sax.ContentHandler, metadata: org.apache.tika.metadata.Metadata, parseContext: org.apache.tika.parser.ParseContext) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.parser.code")``.

    SourceCodeParser: typing.Type[SourceCodeParser]
