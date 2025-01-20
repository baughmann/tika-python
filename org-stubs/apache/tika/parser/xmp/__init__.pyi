
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import org.apache.jempbox.xmp
import org.apache.tika.metadata
import org.apache.xmpbox
import typing



class JempboxExtractor:
    def __init__(self, metadata: org.apache.tika.metadata.Metadata): ...
    @staticmethod
    def extractDublinCore(xMPMetadata: org.apache.jempbox.xmp.XMPMetadata, metadata: org.apache.tika.metadata.Metadata) -> None: ...
    @staticmethod
    def extractXMPMM(xMPMetadata: org.apache.jempbox.xmp.XMPMetadata, metadata: org.apache.tika.metadata.Metadata) -> None: ...
    @staticmethod
    def getMaxXMPMMHistory() -> int: ...
    def parse(self, inputStream: java.io.InputStream) -> None: ...
    @staticmethod
    def setMaxXMPMMHistory(int: int) -> None: ...

class XMPMetadataExtractor:
    def __init__(self): ...
    @staticmethod
    def extractDublinCoreSchema(xMPMetadata: org.apache.xmpbox.XMPMetadata, metadata: org.apache.tika.metadata.Metadata) -> None: ...
    @staticmethod
    def extractXMPBasicSchema(xMPMetadata: org.apache.xmpbox.XMPMetadata, metadata: org.apache.tika.metadata.Metadata) -> None: ...
    @staticmethod
    def parse(inputStream: java.io.InputStream, metadata: org.apache.tika.metadata.Metadata) -> None: ...

class XMPPacketScanner:
    def __init__(self): ...
    def parse(self, inputStream: java.io.InputStream, outputStream: java.io.OutputStream) -> bool: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.parser.xmp")``.

    JempboxExtractor: typing.Type[JempboxExtractor]
    XMPMetadataExtractor: typing.Type[XMPMetadataExtractor]
    XMPPacketScanner: typing.Type[XMPPacketScanner]
