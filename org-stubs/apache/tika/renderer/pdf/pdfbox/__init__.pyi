
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.util
import org.apache.pdfbox.pdmodel
import org.apache.pdfbox.rendering
import org.apache.tika.config
import org.apache.tika.io
import org.apache.tika.metadata
import org.apache.tika.mime
import org.apache.tika.parser
import org.apache.tika.renderer
import typing



class NoTextPDFRenderer(org.apache.pdfbox.rendering.PDFRenderer):
    def __init__(self, pDDocument: org.apache.pdfbox.pdmodel.PDDocument): ...

class PDDocumentRenderer(org.apache.tika.renderer.Renderer): ...

class PDFRenderingState(org.apache.tika.renderer.RenderingState):
    def __init__(self, tikaInputStream: org.apache.tika.io.TikaInputStream): ...
    def getRenderResults(self) -> org.apache.tika.renderer.RenderResults: ...
    def getTikaInputStream(self) -> org.apache.tika.io.TikaInputStream: ...
    def setRenderResults(self, renderResults: org.apache.tika.renderer.RenderResults) -> None: ...

class TextOnlyPDFRenderer(org.apache.pdfbox.rendering.PDFRenderer):
    def __init__(self, pDDocument: org.apache.pdfbox.pdmodel.PDDocument): ...

class VectorGraphicsOnlyPDFRenderer(org.apache.pdfbox.rendering.PDFRenderer):
    def __init__(self, pDDocument: org.apache.pdfbox.pdmodel.PDDocument): ...

class PDFBoxRenderer(PDDocumentRenderer, org.apache.tika.config.Initializable):
    PDFBOX_RENDERING_TIME_MS: typing.ClassVar[org.apache.tika.metadata.Property] = ...
    PDFBOX_IMAGE_WRITING_TIME_MS: typing.ClassVar[org.apache.tika.metadata.Property] = ...
    def __init__(self): ...
    def checkInitialization(self, initializableProblemHandler: typing.Union[org.apache.tika.config.InitializableProblemHandler, typing.Callable]) -> None: ...
    def getSupportedTypes(self, parseContext: org.apache.tika.parser.ParseContext) -> java.util.Set[org.apache.tika.mime.MediaType]: ...
    def initialize(self, map: typing.Union[java.util.Map[str, org.apache.tika.config.Param], typing.Mapping[str, org.apache.tika.config.Param]]) -> None: ...
    def render(self, inputStream: java.io.InputStream, metadata: org.apache.tika.metadata.Metadata, parseContext: org.apache.tika.parser.ParseContext, *renderRequest: org.apache.tika.renderer.RenderRequest) -> org.apache.tika.renderer.RenderResults: ...
    def setDPI(self, int: int) -> None: ...
    def setImageFormatName(self, string: str) -> None: ...
    def setImageType(self, imageType: org.apache.pdfbox.rendering.ImageType) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.renderer.pdf.pdfbox")``.

    NoTextPDFRenderer: typing.Type[NoTextPDFRenderer]
    PDDocumentRenderer: typing.Type[PDDocumentRenderer]
    PDFBoxRenderer: typing.Type[PDFBoxRenderer]
    PDFRenderingState: typing.Type[PDFRenderingState]
    TextOnlyPDFRenderer: typing.Type[TextOnlyPDFRenderer]
    VectorGraphicsOnlyPDFRenderer: typing.Type[VectorGraphicsOnlyPDFRenderer]
