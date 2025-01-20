
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import jpype.protocol
import typing



class ZipSalvager:
    def __init__(self): ...
    @typing.overload
    @staticmethod
    def salvageCopy(file: typing.Union[java.io.File, jpype.protocol.SupportsPath], file2: typing.Union[java.io.File, jpype.protocol.SupportsPath]) -> None: ...
    @typing.overload
    @staticmethod
    def salvageCopy(inputStream: java.io.InputStream, file: typing.Union[java.io.File, jpype.protocol.SupportsPath], boolean: bool) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.zip.utils")``.

    ZipSalvager: typing.Type[ZipSalvager]
