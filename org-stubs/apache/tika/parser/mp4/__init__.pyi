
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import com.drew.imaging.mp4
import com.drew.metadata
import com.drew.metadata.mp4
import java.io
import java.util
import jpype
import org.apache.tika.metadata
import org.apache.tika.mime
import org.apache.tika.parser
import org.apache.tika.parser.mp4.boxes
import org.apache.tika.sax
import org.xml.sax
import typing



class MP4Parser(org.apache.tika.parser.Parser):
    def __init__(self): ...
    def getSupportedTypes(self, parseContext: org.apache.tika.parser.ParseContext) -> java.util.Set[org.apache.tika.mime.MediaType]: ...
    def parse(self, inputStream: java.io.InputStream, contentHandler: org.xml.sax.ContentHandler, metadata: org.apache.tika.metadata.Metadata, parseContext: org.apache.tika.parser.ParseContext) -> None: ...

class TikaMp4BoxHandler(com.drew.metadata.mp4.Mp4BoxHandler):
    def __init__(self, metadata: com.drew.metadata.Metadata, metadata2: org.apache.tika.metadata.Metadata, xHTMLContentHandler: org.apache.tika.sax.XHTMLContentHandler): ...
    def processBox(self, string: str, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], long: int, mp4Context: com.drew.metadata.mp4.Mp4Context) -> com.drew.imaging.mp4.Mp4Handler[typing.Any]: ...
    def shouldAcceptBox(self, string: str) -> bool: ...
    def shouldAcceptContainer(self, string: str) -> bool: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.parser.mp4")``.

    MP4Parser: typing.Type[MP4Parser]
    TikaMp4BoxHandler: typing.Type[TikaMp4BoxHandler]
    boxes: org.apache.tika.parser.mp4.boxes.__module_protocol__
