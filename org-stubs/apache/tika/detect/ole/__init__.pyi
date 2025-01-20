
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import org.apache.tika.detect
import org.apache.tika.metadata
import org.apache.tika.mime
import typing



class MiscOLEDetector(org.apache.tika.detect.Detector):
    OLE: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    HWP: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    QUATTROPRO: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    def __init__(self): ...
    def detect(self, inputStream: java.io.InputStream, metadata: org.apache.tika.metadata.Metadata) -> org.apache.tika.mime.MediaType: ...
    def setMarkLimit(self, int: int) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.detect.ole")``.

    MiscOLEDetector: typing.Type[MiscOLEDetector]
