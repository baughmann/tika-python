
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.util
import org.apache.poi.poifs.filesystem
import org.apache.tika.detect
import org.apache.tika.detect.microsoft.ooxml
import org.apache.tika.metadata
import org.apache.tika.mime
import typing



class POIFSContainerDetector(org.apache.tika.detect.Detector):
    OLE: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    OOXML_PROTECTED: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    DRM_ENCRYPTED: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    GENERAL_EMBEDDED: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    OLE10_NATIVE: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    COMP_OBJ: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    MS_GRAPH_CHART: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    MS_EQUATION: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    OCX_NAME: typing.ClassVar[str] = ...
    XLS: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    DOC: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    PPT: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    PUB: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    VSD: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    WPS: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    XLR: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    MSG: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    MPP: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    SDC: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    SDA: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    SDD: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    SDW: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    SLDWORKS: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    ESRI_LAYER: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    DGN_8: typing.ClassVar[org.apache.tika.mime.MediaType] = ...
    def __init__(self): ...
    @typing.overload
    def detect(self, inputStream: java.io.InputStream, metadata: org.apache.tika.metadata.Metadata) -> org.apache.tika.mime.MediaType: ...
    @typing.overload
    @staticmethod
    def detect(set: java.util.Set[str], directoryEntry: org.apache.poi.poifs.filesystem.DirectoryEntry) -> org.apache.tika.mime.MediaType: ...
    def setMarkLimit(self, int: int) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.detect.microsoft")``.

    POIFSContainerDetector: typing.Type[POIFSContainerDetector]
    ooxml: org.apache.tika.detect.microsoft.ooxml.__module_protocol__
