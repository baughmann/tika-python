
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.nio.file
import java.util
import jpype.protocol
import org.w3c.dom
import typing



class ClassLoaderUtil:
    def __init__(self): ...
    _buildClass__T = typing.TypeVar('_buildClass__T')  # <T>
    @staticmethod
    def buildClass(class_: typing.Type[_buildClass__T], string: str) -> _buildClass__T: ...

class DurationFormatUtils:
    def __init__(self): ...
    @staticmethod
    def formatMillis(long: int) -> str: ...

class PropsUtil:
    def __init__(self): ...
    @staticmethod
    def getBoolean(string: str, boolean: bool) -> bool: ...
    @staticmethod
    def getInt(string: str, integer: int) -> int: ...
    @staticmethod
    def getLong(string: str, long: int) -> int: ...
    @staticmethod
    def getPath(string: str, path: typing.Union[java.nio.file.Path, jpype.protocol.SupportsPath]) -> java.nio.file.Path: ...
    @staticmethod
    def getString(string: str, string2: str) -> str: ...

class XMLDOMUtil:
    def __init__(self): ...
    @staticmethod
    def getInt(string: str, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]], node: org.w3c.dom.Node) -> int: ...
    @staticmethod
    def getLong(string: str, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]], node: org.w3c.dom.Node) -> int: ...
    @staticmethod
    def mapifyAttrs(node: org.w3c.dom.Node, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]]) -> java.util.Map[str, str]: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.util")``.

    ClassLoaderUtil: typing.Type[ClassLoaderUtil]
    DurationFormatUtils: typing.Type[DurationFormatUtils]
    PropsUtil: typing.Type[PropsUtil]
    XMLDOMUtil: typing.Type[XMLDOMUtil]
