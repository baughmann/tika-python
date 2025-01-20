
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import org.apache.tika.metadata
import org.apache.tika.parser
import typing



class CompositeDigester(org.apache.tika.parser.DigestingParser.Digester):
    def __init__(self, *digester: typing.Union[org.apache.tika.parser.DigestingParser.Digester, typing.Callable]): ...
    def digest(self, inputStream: java.io.InputStream, metadata: org.apache.tika.metadata.Metadata, parseContext: org.apache.tika.parser.ParseContext) -> None: ...

class InputStreamDigester(org.apache.tika.parser.DigestingParser.Digester):
    @typing.overload
    def __init__(self, int: int, string: str, string2: str, encoder: typing.Union[org.apache.tika.parser.DigestingParser.Encoder, typing.Callable]): ...
    @typing.overload
    def __init__(self, int: int, string: str, encoder: typing.Union[org.apache.tika.parser.DigestingParser.Encoder, typing.Callable]): ...
    def digest(self, inputStream: java.io.InputStream, metadata: org.apache.tika.metadata.Metadata, parseContext: org.apache.tika.parser.ParseContext) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.parser.digest")``.

    CompositeDigester: typing.Type[CompositeDigester]
    InputStreamDigester: typing.Type[InputStreamDigester]
