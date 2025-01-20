
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.net
import java.nio.file
import jpype
import jpype.protocol
import org.apache.tika.async_
import org.apache.tika.batch
import org.apache.tika.cli
import org.apache.tika.concurrent
import org.apache.tika.config
import org.apache.tika.detect
import org.apache.tika.embedder
import org.apache.tika.exception
import org.apache.tika.extractor
import org.apache.tika.fork
import org.apache.tika.gui
import org.apache.tika.io
import org.apache.tika.langdetect
import org.apache.tika.language
import org.apache.tika.language.translate
import org.apache.tika.metadata
import org.apache.tika.mime
import org.apache.tika.parser
import org.apache.tika.pipes
import org.apache.tika.renderer
import org.apache.tika.sax
import org.apache.tika.serialization
import org.apache.tika.util
import org.apache.tika.utils
import org.apache.tika.xmp
import org.apache.tika.zip
import typing



class Tika:
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, tikaConfig: org.apache.tika.config.TikaConfig): ...
    @typing.overload
    def __init__(self, detector: typing.Union[org.apache.tika.detect.Detector, typing.Callable]): ...
    @typing.overload
    def __init__(self, detector: typing.Union[org.apache.tika.detect.Detector, typing.Callable], parser: org.apache.tika.parser.Parser): ...
    @typing.overload
    def __init__(self, detector: typing.Union[org.apache.tika.detect.Detector, typing.Callable], parser: org.apache.tika.parser.Parser, translator: org.apache.tika.language.translate.Translator): ...
    @typing.overload
    def detect(self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> str: ...
    @typing.overload
    def detect(self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], string: str) -> str: ...
    @typing.overload
    def detect(self, file: typing.Union[java.io.File, jpype.protocol.SupportsPath]) -> str: ...
    @typing.overload
    def detect(self, inputStream: java.io.InputStream) -> str: ...
    @typing.overload
    def detect(self, inputStream: java.io.InputStream, string: str) -> str: ...
    @typing.overload
    def detect(self, inputStream: java.io.InputStream, metadata: org.apache.tika.metadata.Metadata) -> str: ...
    @typing.overload
    def detect(self, string: str) -> str: ...
    @typing.overload
    def detect(self, uRL: java.net.URL) -> str: ...
    @typing.overload
    def detect(self, path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath]) -> str: ...
    def getDetector(self) -> org.apache.tika.detect.Detector: ...
    def getMaxStringLength(self) -> int: ...
    def getParser(self) -> org.apache.tika.parser.Parser: ...
    @staticmethod
    def getString() -> str: ...
    def getTranslator(self) -> org.apache.tika.language.translate.Translator: ...
    @typing.overload
    def parse(self, file: typing.Union[java.io.File, jpype.protocol.SupportsPath]) -> java.io.Reader: ...
    @typing.overload
    def parse(self, file: typing.Union[java.io.File, jpype.protocol.SupportsPath], metadata: org.apache.tika.metadata.Metadata) -> java.io.Reader: ...
    @typing.overload
    def parse(self, inputStream: java.io.InputStream) -> java.io.Reader: ...
    @typing.overload
    def parse(self, inputStream: java.io.InputStream, metadata: org.apache.tika.metadata.Metadata) -> java.io.Reader: ...
    @typing.overload
    def parse(self, uRL: java.net.URL) -> java.io.Reader: ...
    @typing.overload
    def parse(self, path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath]) -> java.io.Reader: ...
    @typing.overload
    def parse(self, path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath], metadata: org.apache.tika.metadata.Metadata) -> java.io.Reader: ...
    @typing.overload
    def parseToString(self, file: typing.Union[java.io.File, jpype.protocol.SupportsPath]) -> str: ...
    @typing.overload
    def parseToString(self, inputStream: java.io.InputStream) -> str: ...
    @typing.overload
    def parseToString(self, inputStream: java.io.InputStream, metadata: org.apache.tika.metadata.Metadata) -> str: ...
    @typing.overload
    def parseToString(self, inputStream: java.io.InputStream, metadata: org.apache.tika.metadata.Metadata, int: int) -> str: ...
    @typing.overload
    def parseToString(self, uRL: java.net.URL) -> str: ...
    @typing.overload
    def parseToString(self, path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath]) -> str: ...
    def setMaxStringLength(self, int: int) -> None: ...
    def toString(self) -> str: ...
    @typing.overload
    def translate(self, string: str, string2: str) -> str: ...
    @typing.overload
    def translate(self, string: str, string2: str, string3: str) -> str: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika")``.

    Tika: typing.Type[Tika]
    async_: org.apache.tika.async_.__module_protocol__
    batch: org.apache.tika.batch.__module_protocol__
    cli: org.apache.tika.cli.__module_protocol__
    concurrent: org.apache.tika.concurrent.__module_protocol__
    config: org.apache.tika.config.__module_protocol__
    detect: org.apache.tika.detect.__module_protocol__
    embedder: org.apache.tika.embedder.__module_protocol__
    exception: org.apache.tika.exception.__module_protocol__
    extractor: org.apache.tika.extractor.__module_protocol__
    fork: org.apache.tika.fork.__module_protocol__
    gui: org.apache.tika.gui.__module_protocol__
    io: org.apache.tika.io.__module_protocol__
    langdetect: org.apache.tika.langdetect.__module_protocol__
    language: org.apache.tika.language.__module_protocol__
    metadata: org.apache.tika.metadata.__module_protocol__
    mime: org.apache.tika.mime.__module_protocol__
    parser: org.apache.tika.parser.__module_protocol__
    pipes: org.apache.tika.pipes.__module_protocol__
    renderer: org.apache.tika.renderer.__module_protocol__
    sax: org.apache.tika.sax.__module_protocol__
    serialization: org.apache.tika.serialization.__module_protocol__
    util: org.apache.tika.util.__module_protocol__
    utils: org.apache.tika.utils.__module_protocol__
    xmp: org.apache.tika.xmp.__module_protocol__
    zip: org.apache.tika.zip.__module_protocol__
