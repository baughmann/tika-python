
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.util
import org.apache.tika.metadata
import org.apache.tika.mime
import org.apache.tika.parser
import org.apache.tika.renderer
import typing



class MuPDFRenderer(org.apache.tika.renderer.Renderer):
    def __init__(self): ...
    def getSupportedTypes(self, parseContext: org.apache.tika.parser.ParseContext) -> java.util.Set[org.apache.tika.mime.MediaType]: ...
    def render(self, inputStream: java.io.InputStream, metadata: org.apache.tika.metadata.Metadata, parseContext: org.apache.tika.parser.ParseContext, *renderRequest: org.apache.tika.renderer.RenderRequest) -> org.apache.tika.renderer.RenderResults: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.renderer.pdf.mutool")``.

    MuPDFRenderer: typing.Type[MuPDFRenderer]
