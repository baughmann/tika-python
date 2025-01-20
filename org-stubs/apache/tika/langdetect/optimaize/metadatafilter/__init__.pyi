
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import org.apache.tika.metadata
import org.apache.tika.metadata.filter
import typing



class OptimaizeMetadataFilter(org.apache.tika.metadata.filter.MetadataFilter):
    def __init__(self): ...
    def filter(self, metadata: org.apache.tika.metadata.Metadata) -> None: ...
    def setMaxCharsForDetection(self, int: int) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.langdetect.optimaize.metadatafilter")``.

    OptimaizeMetadataFilter: typing.Type[OptimaizeMetadataFilter]
