
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import com.drew.metadata.mp4
import jpype
import org.apache.tika.metadata
import org.apache.tika.sax
import typing



class TikaUserDataBox:
    def __init__(self, string: str, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], metadata: org.apache.tika.metadata.Metadata, xHTMLContentHandler: org.apache.tika.sax.XHTMLContentHandler): ...
    def addMetadata(self, mp4Directory: com.drew.metadata.mp4.Mp4Directory) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.parser.mp4.boxes")``.

    TikaUserDataBox: typing.Type[TikaUserDataBox]
