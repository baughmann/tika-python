
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import java.lang.annotation
import java.lang.reflect
import java.net
import java.nio.charset
import java.nio.file
import java.util
import java.util.concurrent
import jpype.protocol
import org.apache.tika.detect
import org.apache.tika.language.translate
import org.apache.tika.metadata.filter
import org.apache.tika.mime
import org.apache.tika.parser
import org.w3c.dom
import typing



class ConfigBase:
    def __init__(self): ...

class Field(java.lang.annotation.Annotation):
    def equals(self, object: typing.Any) -> bool: ...
    def hashCode(self) -> int: ...
    def name(self) -> str: ...
    def required(self) -> bool: ...
    def toString(self) -> str: ...

class Initializable:
    def checkInitialization(self, initializableProblemHandler: typing.Union['InitializableProblemHandler', typing.Callable]) -> None: ...
    def initialize(self, map: typing.Union[java.util.Map[str, 'Param'], typing.Mapping[str, 'Param']]) -> None: ...

class InitializableProblemHandler:
    IGNORE: typing.ClassVar['InitializableProblemHandler'] = ...
    INFO: typing.ClassVar['InitializableProblemHandler'] = ...
    WARN: typing.ClassVar['InitializableProblemHandler'] = ...
    THROW: typing.ClassVar['InitializableProblemHandler'] = ...
    DEFAULT: typing.ClassVar['InitializableProblemHandler'] = ...
    def handleInitializableProblem(self, string: str, string2: str) -> None: ...

class LoadErrorHandler:
    IGNORE: typing.ClassVar['LoadErrorHandler'] = ...
    WARN: typing.ClassVar['LoadErrorHandler'] = ...
    THROW: typing.ClassVar['LoadErrorHandler'] = ...
    def handleLoadError(self, string: str, throwable: java.lang.Throwable) -> None: ...

_Param__T = typing.TypeVar('_Param__T')  # <T>
class Param(java.io.Serializable, typing.Generic[_Param__T]):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: str, class_: typing.Type[_Param__T], t: _Param__T): ...
    @typing.overload
    def __init__(self, string: str, t: _Param__T): ...
    def getName(self) -> str: ...
    def getType(self) -> typing.Type[_Param__T]: ...
    def getTypeString(self) -> str: ...
    def getValue(self) -> _Param__T: ...
    _load_0__T = typing.TypeVar('_load_0__T')  # <T>
    _load_1__T = typing.TypeVar('_load_1__T')  # <T>
    @typing.overload
    @staticmethod
    def load(inputStream: java.io.InputStream) -> 'Param'[_load_0__T]: ...
    @typing.overload
    @staticmethod
    def load(node: org.w3c.dom.Node) -> 'Param'[_load_1__T]: ...
    @typing.overload
    def save(self, outputStream: java.io.OutputStream) -> None: ...
    @typing.overload
    def save(self, document: org.w3c.dom.Document, node: org.w3c.dom.Node) -> None: ...
    def setName(self, string: str) -> None: ...
    def setType(self, class_: typing.Type[_Param__T]) -> None: ...
    def setTypeString(self, string: str) -> None: ...
    def toString(self) -> str: ...

class ParamField:
    DEFAULT: typing.ClassVar[str] = ...
    def __init__(self, accessibleObject: java.lang.reflect.AccessibleObject): ...
    def assignValue(self, object: typing.Any, object2: typing.Any) -> None: ...
    def getField(self) -> java.lang.reflect.Field: ...
    def getName(self) -> str: ...
    def getSetter(self) -> java.lang.reflect.Method: ...
    def getType(self) -> typing.Type[typing.Any]: ...
    def isRequired(self) -> bool: ...
    def toString(self) -> str: ...

class ServiceLoader:
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, classLoader: java.lang.ClassLoader): ...
    @typing.overload
    def __init__(self, classLoader: java.lang.ClassLoader, loadErrorHandler: typing.Union[LoadErrorHandler, typing.Callable]): ...
    @typing.overload
    def __init__(self, classLoader: java.lang.ClassLoader, loadErrorHandler: typing.Union[LoadErrorHandler, typing.Callable], boolean: bool): ...
    @typing.overload
    def __init__(self, classLoader: java.lang.ClassLoader, loadErrorHandler: typing.Union[LoadErrorHandler, typing.Callable], initializableProblemHandler: typing.Union[InitializableProblemHandler, typing.Callable], boolean: bool): ...
    def findServiceResources(self, string: str) -> java.util.Enumeration[java.net.URL]: ...
    def getInitializableProblemHandler(self) -> InitializableProblemHandler: ...
    def getLoadErrorHandler(self) -> LoadErrorHandler: ...
    def getLoader(self) -> java.lang.ClassLoader: ...
    def getResourceAsStream(self, string: str) -> java.io.InputStream: ...
    _getServiceClass__T = typing.TypeVar('_getServiceClass__T')  # <T>
    def getServiceClass(self, class_: typing.Type[_getServiceClass__T], string: str) -> typing.Type[_getServiceClass__T]: ...
    def isDynamic(self) -> bool: ...
    _loadDynamicServiceProviders__T = typing.TypeVar('_loadDynamicServiceProviders__T')  # <T>
    def loadDynamicServiceProviders(self, class_: typing.Type[_loadDynamicServiceProviders__T]) -> java.util.List[_loadDynamicServiceProviders__T]: ...
    _loadServiceProviders__T = typing.TypeVar('_loadServiceProviders__T')  # <T>
    def loadServiceProviders(self, class_: typing.Type[_loadServiceProviders__T]) -> java.util.List[_loadServiceProviders__T]: ...
    _loadStaticServiceProviders_0__T = typing.TypeVar('_loadStaticServiceProviders_0__T')  # <T>
    _loadStaticServiceProviders_1__T = typing.TypeVar('_loadStaticServiceProviders_1__T')  # <T>
    @typing.overload
    def loadStaticServiceProviders(self, class_: typing.Type[_loadStaticServiceProviders_0__T]) -> java.util.List[_loadStaticServiceProviders_0__T]: ...
    @typing.overload
    def loadStaticServiceProviders(self, class_: typing.Type[_loadStaticServiceProviders_1__T], collection: typing.Union[java.util.Collection[typing.Type[_loadStaticServiceProviders_1__T]], typing.Sequence[typing.Type[_loadStaticServiceProviders_1__T]], typing.Set[typing.Type[_loadStaticServiceProviders_1__T]]]) -> java.util.List[_loadStaticServiceProviders_1__T]: ...
    @staticmethod
    def setContextClassLoader(classLoader: java.lang.ClassLoader) -> None: ...

class TikaConfig:
    DEFAULT_MAX_JSON_STRING_FIELD_LENGTH: typing.ClassVar[int] = ...
    MAX_JSON_STRING_FIELD_LENGTH_ELEMENT_NAME: typing.ClassVar[str] = ...
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, file: typing.Union[java.io.File, jpype.protocol.SupportsPath]): ...
    @typing.overload
    def __init__(self, file: typing.Union[java.io.File, jpype.protocol.SupportsPath], serviceLoader: ServiceLoader): ...
    @typing.overload
    def __init__(self, inputStream: java.io.InputStream): ...
    @typing.overload
    def __init__(self, classLoader: java.lang.ClassLoader): ...
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def __init__(self, uRL: java.net.URL): ...
    @typing.overload
    def __init__(self, uRL: java.net.URL, classLoader: java.lang.ClassLoader): ...
    @typing.overload
    def __init__(self, uRL: java.net.URL, serviceLoader: ServiceLoader): ...
    @typing.overload
    def __init__(self, path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath]): ...
    @typing.overload
    def __init__(self, path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath], serviceLoader: ServiceLoader): ...
    @typing.overload
    def __init__(self, document: org.w3c.dom.Document): ...
    @typing.overload
    def __init__(self, document: org.w3c.dom.Document, serviceLoader: ServiceLoader): ...
    @typing.overload
    def __init__(self, element: org.w3c.dom.Element): ...
    @typing.overload
    def __init__(self, element: org.w3c.dom.Element, classLoader: java.lang.ClassLoader): ...
    def getAutoDetectParserConfig(self) -> org.apache.tika.parser.AutoDetectParserConfig: ...
    @staticmethod
    def getDefaultConfig() -> 'TikaConfig': ...
    def getDetector(self) -> org.apache.tika.detect.Detector: ...
    def getEncodingDetector(self) -> org.apache.tika.detect.EncodingDetector: ...
    def getExecutorService(self) -> java.util.concurrent.ExecutorService: ...
    @staticmethod
    def getMaxJsonStringFieldLength() -> int: ...
    def getMediaTypeRegistry(self) -> org.apache.tika.mime.MediaTypeRegistry: ...
    def getMetadataFilter(self) -> org.apache.tika.metadata.filter.MetadataFilter: ...
    def getMimeRepository(self) -> org.apache.tika.mime.MimeTypes: ...
    def getParser(self) -> org.apache.tika.parser.Parser: ...
    def getServiceLoader(self) -> ServiceLoader: ...
    def getTranslator(self) -> org.apache.tika.language.translate.Translator: ...
    @typing.overload
    @staticmethod
    def mustNotBeEmpty(string: str, string2: str) -> None: ...
    @typing.overload
    @staticmethod
    def mustNotBeEmpty(string: str, path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath]) -> None: ...

class TikaConfigSerializer:
    def __init__(self): ...
    @staticmethod
    def serialize(tikaConfig: TikaConfig, mode: 'TikaConfigSerializer.Mode', writer: java.io.Writer, charset: java.nio.charset.Charset) -> None: ...
    @staticmethod
    def serializeParams(document: org.w3c.dom.Document, element: org.w3c.dom.Element, object: typing.Any) -> None: ...
    class Mode(java.lang.Enum['TikaConfigSerializer.Mode']):
        MINIMAL: typing.ClassVar['TikaConfigSerializer.Mode'] = ...
        CURRENT: typing.ClassVar['TikaConfigSerializer.Mode'] = ...
        STATIC: typing.ClassVar['TikaConfigSerializer.Mode'] = ...
        STATIC_FULL: typing.ClassVar['TikaConfigSerializer.Mode'] = ...
        _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'TikaConfigSerializer.Mode': ...
        @staticmethod
        def values() -> typing.MutableSequence['TikaConfigSerializer.Mode']: ...

class TikaTaskTimeout:
    def __init__(self, long: int): ...
    @typing.overload
    def getTimeoutMillis(self) -> int: ...
    @typing.overload
    @staticmethod
    def getTimeoutMillis(parseContext: org.apache.tika.parser.ParseContext, long: int) -> int: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.config")``.

    ConfigBase: typing.Type[ConfigBase]
    Field: typing.Type[Field]
    Initializable: typing.Type[Initializable]
    InitializableProblemHandler: typing.Type[InitializableProblemHandler]
    LoadErrorHandler: typing.Type[LoadErrorHandler]
    Param: typing.Type[Param]
    ParamField: typing.Type[ParamField]
    ServiceLoader: typing.Type[ServiceLoader]
    TikaConfig: typing.Type[TikaConfig]
    TikaConfigSerializer: typing.Type[TikaConfigSerializer]
    TikaTaskTimeout: typing.Type[TikaTaskTimeout]
