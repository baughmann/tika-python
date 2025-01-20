
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.util
import org.apache.tika.config
import typing



class Translator:
    def isAvailable(self) -> bool: ...
    @typing.overload
    def translate(self, string: str, string2: str) -> str: ...
    @typing.overload
    def translate(self, string: str, string2: str, string3: str) -> str: ...

class DefaultTranslator(Translator):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, serviceLoader: org.apache.tika.config.ServiceLoader): ...
    def getTranslator(self) -> Translator: ...
    def getTranslators(self) -> java.util.List[Translator]: ...
    def isAvailable(self) -> bool: ...
    @typing.overload
    def translate(self, string: str, string2: str) -> str: ...
    @typing.overload
    def translate(self, string: str, string2: str, string3: str) -> str: ...

class EmptyTranslator(Translator):
    def __init__(self): ...
    def isAvailable(self) -> bool: ...
    @typing.overload
    def translate(self, string: str, string2: str) -> str: ...
    @typing.overload
    def translate(self, string: str, string2: str, string3: str) -> str: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.language.translate")``.

    DefaultTranslator: typing.Type[DefaultTranslator]
    EmptyTranslator: typing.Type[EmptyTranslator]
    Translator: typing.Type[Translator]
