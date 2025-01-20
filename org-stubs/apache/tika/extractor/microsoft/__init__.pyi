
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import org.apache.tika.extractor
import org.apache.tika.metadata
import typing



class MSEmbeddedStreamTranslator(org.apache.tika.extractor.EmbeddedStreamTranslator):
    def __init__(self): ...
    def shouldTranslate(self, inputStream: java.io.InputStream, metadata: org.apache.tika.metadata.Metadata) -> bool: ...
    def translate(self, inputStream: java.io.InputStream, metadata: org.apache.tika.metadata.Metadata) -> java.io.InputStream: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.extractor.microsoft")``.

    MSEmbeddedStreamTranslator: typing.Type[MSEmbeddedStreamTranslator]
