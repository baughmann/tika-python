
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.nio.charset
import org.apache.tika.detect
import org.apache.tika.metadata
import org.apache.tika.parser.html.charsetdetector.charsets
import typing



class StandardHtmlEncodingDetector(org.apache.tika.detect.EncodingDetector):
    def __init__(self): ...
    def detect(self, inputStream: java.io.InputStream, metadata: org.apache.tika.metadata.Metadata) -> java.nio.charset.Charset: ...
    def getMarkLimit(self) -> int: ...
    def setMarkLimit(self, int: int) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.parser.html.charsetdetector")``.

    StandardHtmlEncodingDetector: typing.Type[StandardHtmlEncodingDetector]
    charsets: org.apache.tika.parser.html.charsetdetector.charsets.__module_protocol__
