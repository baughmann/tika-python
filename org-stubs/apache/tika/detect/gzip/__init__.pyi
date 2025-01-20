
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



class GZipSpecializationDetector(org.apache.tika.detect.Detector):
    GZ: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    WARC_GZ: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    ARC_GZ: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    def __init__(self): ...
    def detect(self, inputStream: java.io.InputStream, metadata: org.apache.tika.metadata.Metadata) -> org.apache.tika.mime.MediaType: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.detect.gzip")``.

    GZipSpecializationDetector: typing.Type[GZipSpecializationDetector]
