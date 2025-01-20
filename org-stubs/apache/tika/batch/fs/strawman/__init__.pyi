
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.nio.file
import java.util.concurrent
import jpype
import jpype.protocol
import typing



class StrawManTikaAppDriver(java.util.concurrent.Callable[int]):
    def __init__(self, path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath], path2: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath], int: int, path3: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath], stringArray: typing.Union[typing.List[str], jpype.JArray]): ...
    def call(self) -> int: ...
    @staticmethod
    def main(stringArray: typing.Union[typing.List[str], jpype.JArray]) -> None: ...
    @staticmethod
    def usage() -> str: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.batch.fs.strawman")``.

    StrawManTikaAppDriver: typing.Type[StrawManTikaAppDriver]
