
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.util
import org.apache.tika.metadata
import org.apache.tika.parser
import org.apache.tika.pipes.emitter
import typing



class FileSystemEmitter(org.apache.tika.pipes.emitter.AbstractEmitter, org.apache.tika.pipes.emitter.StreamEmitter):
    def __init__(self): ...
    @typing.overload
    def emit(self, list: java.util.List[org.apache.tika.pipes.emitter.EmitData]) -> None: ...
    @typing.overload
    def emit(self, string: str, inputStream: java.io.InputStream, metadata: org.apache.tika.metadata.Metadata, parseContext: org.apache.tika.parser.ParseContext) -> None: ...
    @typing.overload
    def emit(self, string: str, list: java.util.List[org.apache.tika.metadata.Metadata], parseContext: org.apache.tika.parser.ParseContext) -> None: ...
    def setBasePath(self, string: str) -> None: ...
    def setFileExtension(self, string: str) -> None: ...
    def setOnExists(self, string: str) -> None: ...
    def setPrettyPrint(self, boolean: bool) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.pipes.emitter.fs")``.

    FileSystemEmitter: typing.Type[FileSystemEmitter]
