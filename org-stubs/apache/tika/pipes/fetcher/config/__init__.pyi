
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import typing



class AbstractConfig:
    def __init__(self): ...

class FetcherConfigContainer:
    def __init__(self): ...
    def getConfigClassName(self) -> str: ...
    def getJson(self) -> str: ...
    def setConfigClassName(self, string: str) -> 'FetcherConfigContainer': ...
    def setJson(self, string: str) -> 'FetcherConfigContainer': ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.pipes.fetcher.config")``.

    AbstractConfig: typing.Type[AbstractConfig]
    FetcherConfigContainer: typing.Type[FetcherConfigContainer]
