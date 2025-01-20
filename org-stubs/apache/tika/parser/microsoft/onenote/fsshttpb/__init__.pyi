
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.util
import org.apache.tika.metadata
import org.apache.tika.parser.microsoft.onenote
import org.apache.tika.parser.microsoft.onenote.fsshttpb.exception
import org.apache.tika.parser.microsoft.onenote.fsshttpb.property
import org.apache.tika.parser.microsoft.onenote.fsshttpb.streamobj
import org.apache.tika.parser.microsoft.onenote.fsshttpb.streamobj.basic
import org.apache.tika.parser.microsoft.onenote.fsshttpb.unsigned
import org.apache.tika.parser.microsoft.onenote.fsshttpb.util
import org.apache.tika.sax
import typing



class IFSSHTTPBSerializable:
    def serializeToByteList(self) -> java.util.List[int]: ...

class MSOneStorePackage:
    storageIndex: org.apache.tika.parser.microsoft.onenote.fsshttpb.streamobj.StorageIndexDataElementData = ...
    storageManifest: org.apache.tika.parser.microsoft.onenote.fsshttpb.streamobj.StorageManifestDataElementData = ...
    headerCellCellManifest: org.apache.tika.parser.microsoft.onenote.fsshttpb.streamobj.CellManifestDataElementData = ...
    headerCellRevisionManifest: org.apache.tika.parser.microsoft.onenote.fsshttpb.streamobj.RevisionManifestDataElementData = ...
    revisionManifests: java.util.List = ...
    cellManifests: java.util.List = ...
    headerCell: org.apache.tika.parser.microsoft.onenote.fsshttpb.streamobj.basic.HeaderCell = ...
    dataRoot: java.util.List = ...
    OtherFileNodeList: java.util.List = ...
    def __init__(self): ...
    def findStorageIndexCellMapping(self, cellID: org.apache.tika.parser.microsoft.onenote.fsshttpb.streamobj.basic.CellID) -> org.apache.tika.parser.microsoft.onenote.fsshttpb.streamobj.StorageIndexCellMapping: ...
    def findStorageIndexRevisionMapping(self, exGuid: org.apache.tika.parser.microsoft.onenote.fsshttpb.streamobj.basic.ExGuid) -> org.apache.tika.parser.microsoft.onenote.fsshttpb.streamobj.StorageIndexRevisionMapping: ...
    def walkTree(self, oneNoteTreeWalkerOptions: org.apache.tika.parser.microsoft.onenote.OneNoteTreeWalkerOptions, metadata: org.apache.tika.metadata.Metadata, xHTMLContentHandler: org.apache.tika.sax.XHTMLContentHandler) -> None: ...

class MSOneStoreParser:
    def __init__(self): ...
    def parse(self, dataElementPackage: org.apache.tika.parser.microsoft.onenote.fsshttpb.streamobj.DataElementPackage) -> MSOneStorePackage: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.parser.microsoft.onenote.fsshttpb")``.

    IFSSHTTPBSerializable: typing.Type[IFSSHTTPBSerializable]
    MSOneStorePackage: typing.Type[MSOneStorePackage]
    MSOneStoreParser: typing.Type[MSOneStoreParser]
    exception: org.apache.tika.parser.microsoft.onenote.fsshttpb.exception.__module_protocol__
    property: org.apache.tika.parser.microsoft.onenote.fsshttpb.property.__module_protocol__
    streamobj: org.apache.tika.parser.microsoft.onenote.fsshttpb.streamobj.__module_protocol__
    unsigned: org.apache.tika.parser.microsoft.onenote.fsshttpb.unsigned.__module_protocol__
    util: org.apache.tika.parser.microsoft.onenote.fsshttpb.util.__module_protocol__
