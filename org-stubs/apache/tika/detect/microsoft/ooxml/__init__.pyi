
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.util
import org.apache.commons.compress.archivers.zip
import org.apache.poi.openxml4j.opc
import org.apache.tika.detect.zip
import org.apache.tika.io
import org.apache.tika.mime
import typing



class OPCPackageDetector(org.apache.tika.detect.zip.ZipContainerDetector):
    def __init__(self): ...
    def detect(self, zipFile: org.apache.commons.compress.archivers.zip.ZipFile, tikaInputStream: org.apache.tika.io.TikaInputStream) -> org.apache.tika.mime.MediaType: ...
    @staticmethod
    def detectOfficeOpenXML(oPCPackage: org.apache.poi.openxml4j.opc.OPCPackage) -> org.apache.tika.mime.MediaType: ...
    @staticmethod
    def parseOOXMLRels(inputStream: java.io.InputStream) -> java.util.Set[str]: ...
    def streamingDetectFinal(self, streamingDetectContext: org.apache.tika.detect.zip.StreamingDetectContext) -> org.apache.tika.mime.MediaType: ...
    def streamingDetectUpdate(self, zipArchiveEntry: org.apache.commons.compress.archivers.zip.ZipArchiveEntry, inputStream: java.io.InputStream, streamingDetectContext: org.apache.tika.detect.zip.StreamingDetectContext) -> org.apache.tika.mime.MediaType: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.detect.microsoft.ooxml")``.

    OPCPackageDetector: typing.Type[OPCPackageDetector]
