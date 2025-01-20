
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.time.format
import java.util
import org.apache.tika.metadata
import typing



class MailDateParser:
    RFC_5322: typing.ClassVar[java.time.format.DateTimeFormatter] = ...
    RFC_5322_LENIENT: typing.ClassVar[java.time.format.DateTimeFormatter] = ...
    RFC_5322_AMPM_LENIENT: typing.ClassVar[java.time.format.DateTimeFormatter] = ...
    MMM_D_YYYY_HH_MM_AM_PM: typing.ClassVar[java.time.format.DateTimeFormatter] = ...
    MMM_D_YYYY_HH_MM: typing.ClassVar[java.time.format.DateTimeFormatter] = ...
    MM_SLASH_DD_SLASH_YY_HH_MM: typing.ClassVar[java.time.format.DateTimeFormatter] = ...
    MM_SLASH_DD_SLASH_YY_HH_MM_AM_PM: typing.ClassVar[java.time.format.DateTimeFormatter] = ...
    YYYY_MM_DD_HH_MM: typing.ClassVar[java.time.format.DateTimeFormatter] = ...
    YYYY_MM_DD: typing.ClassVar[java.time.format.DateTimeFormatter] = ...
    MM_SLASH_DD_SLASH_YYYY: typing.ClassVar[java.time.format.DateTimeFormatter] = ...
    DD_SLASH_MM_SLASH_YYYY: typing.ClassVar[java.time.format.DateTimeFormatter] = ...
    MMM_DD_YY: typing.ClassVar[java.time.format.DateTimeFormatter] = ...
    DD_MMM_YY: typing.ClassVar[java.time.format.DateTimeFormatter] = ...
    YY_SLASH_MM_SLASH_DD: typing.ClassVar[java.time.format.DateTimeFormatter] = ...
    def __init__(self): ...
    @staticmethod
    def parseDateLenient(string: str) -> java.util.Date: ...
    @staticmethod
    def parseRFC5322(string: str) -> java.util.Date: ...

class MailUtil:
    def __init__(self): ...
    @staticmethod
    def addPersonAndEmail(string: str, property: org.apache.tika.metadata.Property, property2: org.apache.tika.metadata.Property, metadata: org.apache.tika.metadata.Metadata) -> None: ...
    @staticmethod
    def containsEmail(string: str) -> bool: ...
    @staticmethod
    def setPersonAndEmail(string: str, property: org.apache.tika.metadata.Property, property2: org.apache.tika.metadata.Property, metadata: org.apache.tika.metadata.Metadata) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.parser.mailcommons")``.

    MailDateParser: typing.Type[MailDateParser]
    MailUtil: typing.Type[MailUtil]
