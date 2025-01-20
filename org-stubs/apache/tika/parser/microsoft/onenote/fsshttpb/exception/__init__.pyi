
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import typing



class DataElementParseErrorException(java.lang.RuntimeException):
    @typing.overload
    def __init__(self, int: int, exception: java.lang.Exception): ...
    @typing.overload
    def __init__(self, int: int, string: str, exception: java.lang.Exception): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.parser.microsoft.onenote.fsshttpb.exception")``.

    DataElementParseErrorException: typing.Type[DataElementParseErrorException]
