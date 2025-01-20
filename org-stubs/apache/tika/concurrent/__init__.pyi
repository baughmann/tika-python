
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.util.concurrent
import typing



class ConfigurableThreadPoolExecutor(java.util.concurrent.ExecutorService):
    def setCorePoolSize(self, int: int) -> None: ...
    def setMaximumPoolSize(self, int: int) -> None: ...

class SimpleThreadPoolExecutor(java.util.concurrent.ThreadPoolExecutor, ConfigurableThreadPoolExecutor):
    def __init__(self): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.concurrent")``.

    ConfigurableThreadPoolExecutor: typing.Type[ConfigurableThreadPoolExecutor]
    SimpleThreadPoolExecutor: typing.Type[SimpleThreadPoolExecutor]
