
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.util
import java.util.concurrent
import org.apache.commons.cli
import org.apache.tika.batch
import org.apache.tika.sax
import org.w3c.dom
import typing



class AbstractConsumersBuilder:
    def __init__(self): ...
    def build(self, node: org.w3c.dom.Node, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]], arrayBlockingQueue: java.util.concurrent.ArrayBlockingQueue[org.apache.tika.batch.FileResource]) -> org.apache.tika.batch.ConsumersManager: ...
    @staticmethod
    def getDefaultNumConsumers() -> int: ...

class BatchProcessBuilder:
    DEFAULT_MAX_QUEUE_SIZE: typing.ClassVar[int] = ...
    MAX_QUEUE_SIZE_KEY: typing.ClassVar[str] = ...
    NUM_CONSUMERS_KEY: typing.ClassVar[str] = ...
    def __init__(self): ...
    @typing.overload
    def build(self, inputStream: java.io.InputStream, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]]) -> org.apache.tika.batch.BatchProcess: ...
    @typing.overload
    def build(self, node: org.w3c.dom.Node, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]]) -> org.apache.tika.batch.BatchProcess: ...
    @staticmethod
    def getNumConsumers(map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]]) -> int: ...

class CommandLineParserBuilder:
    def __init__(self): ...
    def build(self, inputStream: java.io.InputStream) -> org.apache.commons.cli.Options: ...

class IParserFactoryBuilder:
    def build(self, node: org.w3c.dom.Node, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]]) -> org.apache.tika.batch.ParserFactory: ...

class InterrupterBuilder:
    def __init__(self): ...
    def build(self, node: org.w3c.dom.Node, long: int, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]]) -> org.apache.tika.batch.Interrupter: ...

_ObjectFromDOMAndQueueBuilder__T = typing.TypeVar('_ObjectFromDOMAndQueueBuilder__T')  # <T>
class ObjectFromDOMAndQueueBuilder(typing.Generic[_ObjectFromDOMAndQueueBuilder__T]):
    def build(self, node: org.w3c.dom.Node, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]], arrayBlockingQueue: java.util.concurrent.ArrayBlockingQueue[org.apache.tika.batch.FileResource]) -> _ObjectFromDOMAndQueueBuilder__T: ...

_ObjectFromDOMBuilder__T = typing.TypeVar('_ObjectFromDOMBuilder__T')  # <T>
class ObjectFromDOMBuilder(typing.Generic[_ObjectFromDOMBuilder__T]):
    def build(self, node: org.w3c.dom.Node, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]]) -> _ObjectFromDOMBuilder__T: ...

class StatusReporterBuilder:
    def build(self, fileResourceCrawler: org.apache.tika.batch.FileResourceCrawler, consumersManager: org.apache.tika.batch.ConsumersManager, node: org.w3c.dom.Node, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]]) -> org.apache.tika.batch.StatusReporter: ...

class AppParserFactoryBuilder(IParserFactoryBuilder):
    def __init__(self): ...
    def build(self, node: org.w3c.dom.Node, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]]) -> org.apache.tika.batch.ParserFactory: ...

class IContentHandlerFactoryBuilder(ObjectFromDOMBuilder[org.apache.tika.sax.ContentHandlerFactory]):
    def build(self, node: org.w3c.dom.Node, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]]) -> org.apache.tika.sax.ContentHandlerFactory: ...

class ICrawlerBuilder(ObjectFromDOMAndQueueBuilder[org.apache.tika.batch.FileResourceCrawler]):
    def build(self, node: org.w3c.dom.Node, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]], arrayBlockingQueue: java.util.concurrent.ArrayBlockingQueue[org.apache.tika.batch.FileResource]) -> org.apache.tika.batch.FileResourceCrawler: ...

class ParserFactoryBuilder(IParserFactoryBuilder):
    def __init__(self): ...
    def build(self, node: org.w3c.dom.Node, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]]) -> org.apache.tika.batch.ParserFactory: ...

class ReporterBuilder(ObjectFromDOMBuilder[org.apache.tika.batch.StatusReporter]):
    def build(self, node: org.w3c.dom.Node, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]]) -> org.apache.tika.batch.StatusReporter: ...

class SimpleLogReporterBuilder(StatusReporterBuilder):
    def __init__(self): ...
    def build(self, fileResourceCrawler: org.apache.tika.batch.FileResourceCrawler, consumersManager: org.apache.tika.batch.ConsumersManager, node: org.w3c.dom.Node, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]]) -> org.apache.tika.batch.StatusReporter: ...

class DefaultContentHandlerFactoryBuilder(IContentHandlerFactoryBuilder):
    def __init__(self): ...
    def build(self, node: org.w3c.dom.Node, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]]) -> org.apache.tika.sax.ContentHandlerFactory: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.batch.builders")``.

    AbstractConsumersBuilder: typing.Type[AbstractConsumersBuilder]
    AppParserFactoryBuilder: typing.Type[AppParserFactoryBuilder]
    BatchProcessBuilder: typing.Type[BatchProcessBuilder]
    CommandLineParserBuilder: typing.Type[CommandLineParserBuilder]
    DefaultContentHandlerFactoryBuilder: typing.Type[DefaultContentHandlerFactoryBuilder]
    IContentHandlerFactoryBuilder: typing.Type[IContentHandlerFactoryBuilder]
    ICrawlerBuilder: typing.Type[ICrawlerBuilder]
    IParserFactoryBuilder: typing.Type[IParserFactoryBuilder]
    InterrupterBuilder: typing.Type[InterrupterBuilder]
    ObjectFromDOMAndQueueBuilder: typing.Type[ObjectFromDOMAndQueueBuilder]
    ObjectFromDOMBuilder: typing.Type[ObjectFromDOMBuilder]
    ParserFactoryBuilder: typing.Type[ParserFactoryBuilder]
    ReporterBuilder: typing.Type[ReporterBuilder]
    SimpleLogReporterBuilder: typing.Type[SimpleLogReporterBuilder]
    StatusReporterBuilder: typing.Type[StatusReporterBuilder]
