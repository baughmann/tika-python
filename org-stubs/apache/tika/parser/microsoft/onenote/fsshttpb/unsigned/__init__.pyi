
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import java.math
import typing



class UMath:
    @typing.overload
    @staticmethod
    def max(uByte: 'UByte', uByte2: 'UByte') -> 'UByte': ...
    @typing.overload
    @staticmethod
    def max(uInteger: 'UInteger', uInteger2: 'UInteger') -> 'UInteger': ...
    @typing.overload
    @staticmethod
    def max(uLong: 'ULong', uLong2: 'ULong') -> 'ULong': ...
    @typing.overload
    @staticmethod
    def max(uShort: 'UShort', uShort2: 'UShort') -> 'UShort': ...
    @typing.overload
    @staticmethod
    def min(uByte: 'UByte', uByte2: 'UByte') -> 'UByte': ...
    @typing.overload
    @staticmethod
    def min(uInteger: 'UInteger', uInteger2: 'UInteger') -> 'UInteger': ...
    @typing.overload
    @staticmethod
    def min(uLong: 'ULong', uLong2: 'ULong') -> 'ULong': ...
    @typing.overload
    @staticmethod
    def min(uShort: 'UShort', uShort2: 'UShort') -> 'UShort': ...

class UNumber(java.lang.Number):
    def __init__(self): ...
    def toBigInteger(self) -> java.math.BigInteger: ...

class Unsigned:
    @typing.overload
    @staticmethod
    def ubyte(byte: int) -> 'UByte': ...
    @typing.overload
    @staticmethod
    def ubyte(int: int) -> 'UByte': ...
    @typing.overload
    @staticmethod
    def ubyte(string: str) -> 'UByte': ...
    @typing.overload
    @staticmethod
    def ubyte(long: int) -> 'UByte': ...
    @typing.overload
    @staticmethod
    def ubyte(short: int) -> 'UByte': ...
    @typing.overload
    @staticmethod
    def uint(int: int) -> 'UInteger': ...
    @typing.overload
    @staticmethod
    def uint(string: str) -> 'UInteger': ...
    @typing.overload
    @staticmethod
    def uint(long: int) -> 'UInteger': ...
    @typing.overload
    @staticmethod
    def ulong(string: str) -> 'ULong': ...
    @typing.overload
    @staticmethod
    def ulong(bigInteger: java.math.BigInteger) -> 'ULong': ...
    @typing.overload
    @staticmethod
    def ulong(long: int) -> 'ULong': ...
    @typing.overload
    @staticmethod
    def ushort(int: int) -> 'UShort': ...
    @typing.overload
    @staticmethod
    def ushort(string: str) -> 'UShort': ...
    @typing.overload
    @staticmethod
    def ushort(short: int) -> 'UShort': ...

class UByte(UNumber, java.lang.Comparable['UByte']):
    MIN_VALUE: typing.ClassVar[int] = ...
    MAX_VALUE: typing.ClassVar[int] = ...
    MIN: typing.ClassVar['UByte'] = ...
    MAX: typing.ClassVar['UByte'] = ...
    @typing.overload
    def add(self, int: int) -> 'UByte': ...
    @typing.overload
    def add(self, uByte: 'UByte') -> 'UByte': ...
    def compareTo(self, uByte: 'UByte') -> int: ...
    def doubleValue(self) -> float: ...
    def equals(self, object: typing.Any) -> bool: ...
    def floatValue(self) -> float: ...
    def hashCode(self) -> int: ...
    def intValue(self) -> int: ...
    def longValue(self) -> int: ...
    @typing.overload
    def subtract(self, int: int) -> 'UByte': ...
    @typing.overload
    def subtract(self, uByte: 'UByte') -> 'UByte': ...
    def toBigInteger(self) -> java.math.BigInteger: ...
    def toString(self) -> str: ...
    @typing.overload
    @staticmethod
    def valueOf(byte: int) -> 'UByte': ...
    @typing.overload
    @staticmethod
    def valueOf(int: int) -> 'UByte': ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'UByte': ...
    @typing.overload
    @staticmethod
    def valueOf(long: int) -> 'UByte': ...
    @typing.overload
    @staticmethod
    def valueOf(short: int) -> 'UByte': ...

class UInteger(UNumber, java.lang.Comparable['UInteger']):
    MIN_VALUE: typing.ClassVar[int] = ...
    MAX_VALUE: typing.ClassVar[int] = ...
    MIN: typing.ClassVar['UInteger'] = ...
    MAX: typing.ClassVar['UInteger'] = ...
    @typing.overload
    def add(self, int: int) -> 'UInteger': ...
    @typing.overload
    def add(self, uInteger: 'UInteger') -> 'UInteger': ...
    def compareTo(self, uInteger: 'UInteger') -> int: ...
    def doubleValue(self) -> float: ...
    def equals(self, object: typing.Any) -> bool: ...
    def floatValue(self) -> float: ...
    def hashCode(self) -> int: ...
    @typing.overload
    def inclusiveOr(self, int: int) -> 'UInteger': ...
    @typing.overload
    def inclusiveOr(self, long: int) -> 'UInteger': ...
    @typing.overload
    def inclusiveOr(self, uInteger: 'UInteger') -> 'UInteger': ...
    def intValue(self) -> int: ...
    def leftShift(self, int: int) -> 'UInteger': ...
    def longValue(self) -> int: ...
    def rightShift(self, int: int) -> 'UInteger': ...
    @typing.overload
    def subtract(self, int: int) -> 'UInteger': ...
    @typing.overload
    def subtract(self, uInteger: 'UInteger') -> 'UInteger': ...
    def toBigInteger(self) -> java.math.BigInteger: ...
    def toString(self) -> str: ...
    @typing.overload
    @staticmethod
    def valueOf(int: int) -> 'UInteger': ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'UInteger': ...
    @typing.overload
    @staticmethod
    def valueOf(long: int) -> 'UInteger': ...
    @typing.overload
    def xor(self, int: int) -> 'UInteger': ...
    @typing.overload
    def xor(self, long: int) -> 'UInteger': ...
    @typing.overload
    def xor(self, uInteger: 'UInteger') -> 'UInteger': ...

class ULong(UNumber, java.lang.Comparable['ULong']):
    MIN_VALUE: typing.ClassVar[java.math.BigInteger] = ...
    MAX_VALUE: typing.ClassVar[java.math.BigInteger] = ...
    MAX_VALUE_LONG: typing.ClassVar[java.math.BigInteger] = ...
    MIN: typing.ClassVar['ULong'] = ...
    MAX: typing.ClassVar['ULong'] = ...
    @typing.overload
    def add(self, int: int) -> 'ULong': ...
    @typing.overload
    def add(self, long: int) -> 'ULong': ...
    @typing.overload
    def add(self, uLong: 'ULong') -> 'ULong': ...
    @staticmethod
    def compare(long: int, long2: int) -> int: ...
    def compareTo(self, uLong: 'ULong') -> int: ...
    def doubleValue(self) -> float: ...
    def equals(self, object: typing.Any) -> bool: ...
    def floatValue(self) -> float: ...
    def hashCode(self) -> int: ...
    def intValue(self) -> int: ...
    def longValue(self) -> int: ...
    @typing.overload
    def subtract(self, int: int) -> 'ULong': ...
    @typing.overload
    def subtract(self, long: int) -> 'ULong': ...
    @typing.overload
    def subtract(self, uLong: 'ULong') -> 'ULong': ...
    def toString(self) -> str: ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'ULong': ...
    @typing.overload
    @staticmethod
    def valueOf(bigInteger: java.math.BigInteger) -> 'ULong': ...
    @typing.overload
    @staticmethod
    def valueOf(long: int) -> 'ULong': ...

class UShort(UNumber, java.lang.Comparable['UShort']):
    MIN_VALUE: typing.ClassVar[int] = ...
    MAX_VALUE: typing.ClassVar[int] = ...
    MIN: typing.ClassVar['UShort'] = ...
    MAX: typing.ClassVar['UShort'] = ...
    @typing.overload
    def add(self, int: int) -> 'UShort': ...
    @typing.overload
    def add(self, uShort: 'UShort') -> 'UShort': ...
    def compareTo(self, uShort: 'UShort') -> int: ...
    def doubleValue(self) -> float: ...
    def equals(self, object: typing.Any) -> bool: ...
    def floatValue(self) -> float: ...
    def hashCode(self) -> int: ...
    def intValue(self) -> int: ...
    def longValue(self) -> int: ...
    @typing.overload
    def subtract(self, int: int) -> 'UShort': ...
    @typing.overload
    def subtract(self, uShort: 'UShort') -> 'UShort': ...
    def toBigInteger(self) -> java.math.BigInteger: ...
    def toString(self) -> str: ...
    @typing.overload
    @staticmethod
    def valueOf(int: int) -> 'UShort': ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'UShort': ...
    @typing.overload
    @staticmethod
    def valueOf(short: int) -> 'UShort': ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.parser.microsoft.onenote.fsshttpb.unsigned")``.

    UByte: typing.Type[UByte]
    UInteger: typing.Type[UInteger]
    ULong: typing.Type[ULong]
    UMath: typing.Type[UMath]
    UNumber: typing.Type[UNumber]
    UShort: typing.Type[UShort]
    Unsigned: typing.Type[Unsigned]
