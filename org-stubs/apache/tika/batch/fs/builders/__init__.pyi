
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.util
import java.util.concurrent
import org.apache.tika.batch
import org.apache.tika.batch.builders
import org.w3c.dom
import typing



class BasicTikaFSConsumersBuilder(org.apache.tika.batch.builders.AbstractConsumersBuilder):
    def __init__(self): ...
    def build(self, node: org.w3c.dom.Node, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]], arrayBlockingQueue: java.util.concurrent.ArrayBlockingQueue[org.apache.tika.batch.FileResource]) -> org.apache.tika.batch.ConsumersManager: ...

class FSCrawlerBuilder(org.apache.tika.batch.builders.ICrawlerBuilder):
    def __init__(self): ...
    def build(self, node: org.w3c.dom.Node, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]], arrayBlockingQueue: java.util.concurrent.ArrayBlockingQueue[org.apache.tika.batch.FileResource]) -> org.apache.tika.batch.FileResourceCrawler: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.batch.fs.builders")``.

    BasicTikaFSConsumersBuilder: typing.Type[BasicTikaFSConsumersBuilder]
    FSCrawlerBuilder: typing.Type[FSCrawlerBuilder]
