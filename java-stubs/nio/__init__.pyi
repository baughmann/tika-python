
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import java.nio.channels
import java.nio.charset
import java.nio.file
import java.util.stream
import jpype
import typing



class Buffer:
    def array(self) -> typing.Any: ...
    def arrayOffset(self) -> int: ...
    def capacity(self) -> int: ...
    def clear(self) -> 'Buffer': ...
    def duplicate(self) -> 'Buffer': ...
    def flip(self) -> 'Buffer': ...
    def hasArray(self) -> bool: ...
    def hasRemaining(self) -> bool: ...
    def isDirect(self) -> bool: ...
    def isReadOnly(self) -> bool: ...
    @typing.overload
    def limit(self) -> int: ...
    @typing.overload
    def limit(self, int: int) -> 'Buffer': ...
    def mark(self) -> 'Buffer': ...
    @typing.overload
    def position(self) -> int: ...
    @typing.overload
    def position(self, int: int) -> 'Buffer': ...
    def remaining(self) -> int: ...
    def reset(self) -> 'Buffer': ...
    def rewind(self) -> 'Buffer': ...
    @typing.overload
    def slice(self) -> 'Buffer': ...
    @typing.overload
    def slice(self, int: int, int2: int) -> 'Buffer': ...

class BufferOverflowException(java.lang.RuntimeException):
    def __init__(self): ...

class BufferUnderflowException(java.lang.RuntimeException):
    def __init__(self): ...

class ByteOrder:
    BIG_ENDIAN: typing.ClassVar['ByteOrder'] = ...
    LITTLE_ENDIAN: typing.ClassVar['ByteOrder'] = ...
    @staticmethod
    def nativeOrder() -> 'ByteOrder': ...
    def toString(self) -> str: ...

class InvalidMarkException(java.lang.IllegalStateException):
    def __init__(self): ...

class ReadOnlyBufferException(java.lang.UnsupportedOperationException):
    def __init__(self): ...

class ByteBuffer(Buffer, java.lang.Comparable['ByteBuffer']):
    def alignedSlice(self, int: int) -> 'ByteBuffer': ...
    def alignmentOffset(self, int: int, int2: int) -> int: ...
    @staticmethod
    def allocate(int: int) -> 'ByteBuffer': ...
    @staticmethod
    def allocateDirect(int: int) -> 'ByteBuffer': ...
    def array(self) -> typing.MutableSequence[int]: ...
    def arrayOffset(self) -> int: ...
    def asCharBuffer(self) -> 'CharBuffer': ...
    def asDoubleBuffer(self) -> 'DoubleBuffer': ...
    def asFloatBuffer(self) -> 'FloatBuffer': ...
    def asIntBuffer(self) -> 'IntBuffer': ...
    def asLongBuffer(self) -> 'LongBuffer': ...
    def asReadOnlyBuffer(self) -> 'ByteBuffer': ...
    def asShortBuffer(self) -> 'ShortBuffer': ...
    def clear(self) -> 'ByteBuffer': ...
    def compact(self) -> 'ByteBuffer': ...
    def compareTo(self, byteBuffer: 'ByteBuffer') -> int: ...
    def duplicate(self) -> 'ByteBuffer': ...
    def equals(self, object: typing.Any) -> bool: ...
    def flip(self) -> 'ByteBuffer': ...
    @typing.overload
    def get(self) -> int: ...
    @typing.overload
    def get(self, int: int) -> int: ...
    @typing.overload
    def get(self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> 'ByteBuffer': ...
    @typing.overload
    def get(self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], int: int, int2: int) -> 'ByteBuffer': ...
    @typing.overload
    def get(self, int: int, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> 'ByteBuffer': ...
    @typing.overload
    def get(self, int: int, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], int2: int, int3: int) -> 'ByteBuffer': ...
    @typing.overload
    def getChar(self) -> str: ...
    @typing.overload
    def getChar(self, int: int) -> str: ...
    @typing.overload
    def getDouble(self) -> float: ...
    @typing.overload
    def getDouble(self, int: int) -> float: ...
    @typing.overload
    def getFloat(self) -> float: ...
    @typing.overload
    def getFloat(self, int: int) -> float: ...
    @typing.overload
    def getInt(self) -> int: ...
    @typing.overload
    def getInt(self, int: int) -> int: ...
    @typing.overload
    def getLong(self) -> int: ...
    @typing.overload
    def getLong(self, int: int) -> int: ...
    @typing.overload
    def getShort(self) -> int: ...
    @typing.overload
    def getShort(self, int: int) -> int: ...
    def hasArray(self) -> bool: ...
    def hashCode(self) -> int: ...
    def isDirect(self) -> bool: ...
    @typing.overload
    def limit(self) -> int: ...
    @typing.overload
    def limit(self, int: int) -> 'ByteBuffer': ...
    def mark(self) -> 'ByteBuffer': ...
    def mismatch(self, byteBuffer: 'ByteBuffer') -> int: ...
    @typing.overload
    def order(self, byteOrder: ByteOrder) -> 'ByteBuffer': ...
    @typing.overload
    def order(self) -> ByteOrder: ...
    @typing.overload
    def position(self) -> int: ...
    @typing.overload
    def position(self, int: int) -> 'ByteBuffer': ...
    @typing.overload
    def put(self, byte: int) -> 'ByteBuffer': ...
    @typing.overload
    def put(self, int: int, byte: int) -> 'ByteBuffer': ...
    @typing.overload
    def put(self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> 'ByteBuffer': ...
    @typing.overload
    def put(self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], int: int, int2: int) -> 'ByteBuffer': ...
    @typing.overload
    def put(self, int: int, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> 'ByteBuffer': ...
    @typing.overload
    def put(self, int: int, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], int2: int, int3: int) -> 'ByteBuffer': ...
    @typing.overload
    def put(self, int: int, byteBuffer: 'ByteBuffer', int2: int, int3: int) -> 'ByteBuffer': ...
    @typing.overload
    def put(self, byteBuffer: 'ByteBuffer') -> 'ByteBuffer': ...
    @typing.overload
    def putChar(self, char: str) -> 'ByteBuffer': ...
    @typing.overload
    def putChar(self, int: int, char: str) -> 'ByteBuffer': ...
    @typing.overload
    def putDouble(self, double: float) -> 'ByteBuffer': ...
    @typing.overload
    def putDouble(self, int: int, double: float) -> 'ByteBuffer': ...
    @typing.overload
    def putFloat(self, float: float) -> 'ByteBuffer': ...
    @typing.overload
    def putFloat(self, int: int, float: float) -> 'ByteBuffer': ...
    @typing.overload
    def putInt(self, int: int) -> 'ByteBuffer': ...
    @typing.overload
    def putInt(self, int: int, int2: int) -> 'ByteBuffer': ...
    @typing.overload
    def putLong(self, int: int, long: int) -> 'ByteBuffer': ...
    @typing.overload
    def putLong(self, long: int) -> 'ByteBuffer': ...
    @typing.overload
    def putShort(self, int: int, short: int) -> 'ByteBuffer': ...
    @typing.overload
    def putShort(self, short: int) -> 'ByteBuffer': ...
    def reset(self) -> 'ByteBuffer': ...
    def rewind(self) -> 'ByteBuffer': ...
    @typing.overload
    def slice(self) -> 'ByteBuffer': ...
    @typing.overload
    def slice(self, int: int, int2: int) -> 'ByteBuffer': ...
    def toString(self) -> str: ...
    @typing.overload
    @staticmethod
    def wrap(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> 'ByteBuffer': ...
    @typing.overload
    @staticmethod
    def wrap(byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], int: int, int2: int) -> 'ByteBuffer': ...

class CharBuffer(Buffer, java.lang.Comparable['CharBuffer'], java.lang.Appendable, java.lang.CharSequence, java.lang.Readable):
    @staticmethod
    def allocate(int: int) -> 'CharBuffer': ...
    @typing.overload
    def append(self, char: str) -> 'CharBuffer': ...
    @typing.overload
    def append(self, charSequence: typing.Union[java.lang.CharSequence, str]) -> 'CharBuffer': ...
    @typing.overload
    def append(self, charSequence: typing.Union[java.lang.CharSequence, str], int: int, int2: int) -> 'CharBuffer': ...
    def array(self) -> typing.MutableSequence[str]: ...
    def arrayOffset(self) -> int: ...
    def asReadOnlyBuffer(self) -> 'CharBuffer': ...
    def charAt(self, int: int) -> str: ...
    def chars(self) -> java.util.stream.IntStream: ...
    def clear(self) -> 'CharBuffer': ...
    def compact(self) -> 'CharBuffer': ...
    def compareTo(self, charBuffer: 'CharBuffer') -> int: ...
    def duplicate(self) -> 'CharBuffer': ...
    def equals(self, object: typing.Any) -> bool: ...
    def flip(self) -> 'CharBuffer': ...
    @typing.overload
    def get(self) -> str: ...
    @typing.overload
    def get(self, int: int) -> str: ...
    @typing.overload
    def get(self, charArray: typing.Union[typing.List[str], jpype.JArray]) -> 'CharBuffer': ...
    @typing.overload
    def get(self, charArray: typing.Union[typing.List[str], jpype.JArray], int: int, int2: int) -> 'CharBuffer': ...
    @typing.overload
    def get(self, int: int, charArray: typing.Union[typing.List[str], jpype.JArray]) -> 'CharBuffer': ...
    @typing.overload
    def get(self, int: int, charArray: typing.Union[typing.List[str], jpype.JArray], int2: int, int3: int) -> 'CharBuffer': ...
    def hasArray(self) -> bool: ...
    def hashCode(self) -> int: ...
    def isDirect(self) -> bool: ...
    def isEmpty(self) -> bool: ...
    def length(self) -> int: ...
    @typing.overload
    def limit(self) -> int: ...
    @typing.overload
    def limit(self, int: int) -> 'CharBuffer': ...
    def mark(self) -> 'CharBuffer': ...
    def mismatch(self, charBuffer: 'CharBuffer') -> int: ...
    def order(self) -> ByteOrder: ...
    @typing.overload
    def position(self) -> int: ...
    @typing.overload
    def position(self, int: int) -> 'CharBuffer': ...
    @typing.overload
    def put(self, char: str) -> 'CharBuffer': ...
    @typing.overload
    def put(self, int: int, char: str) -> 'CharBuffer': ...
    @typing.overload
    def put(self, charArray: typing.Union[typing.List[str], jpype.JArray]) -> 'CharBuffer': ...
    @typing.overload
    def put(self, string: str) -> 'CharBuffer': ...
    @typing.overload
    def put(self, charArray: typing.Union[typing.List[str], jpype.JArray], int: int, int2: int) -> 'CharBuffer': ...
    @typing.overload
    def put(self, int: int, charArray: typing.Union[typing.List[str], jpype.JArray]) -> 'CharBuffer': ...
    @typing.overload
    def put(self, int: int, charArray: typing.Union[typing.List[str], jpype.JArray], int2: int, int3: int) -> 'CharBuffer': ...
    @typing.overload
    def put(self, int: int, charBuffer: 'CharBuffer', int2: int, int3: int) -> 'CharBuffer': ...
    @typing.overload
    def put(self, string: str, int: int, int2: int) -> 'CharBuffer': ...
    @typing.overload
    def put(self, charBuffer: 'CharBuffer') -> 'CharBuffer': ...
    def read(self, charBuffer: 'CharBuffer') -> int: ...
    def reset(self) -> 'CharBuffer': ...
    def rewind(self) -> 'CharBuffer': ...
    @typing.overload
    def slice(self) -> 'CharBuffer': ...
    @typing.overload
    def slice(self, int: int, int2: int) -> 'CharBuffer': ...
    def subSequence(self, int: int, int2: int) -> 'CharBuffer': ...
    def toString(self) -> str: ...
    @typing.overload
    @staticmethod
    def wrap(charArray: typing.Union[typing.List[str], jpype.JArray]) -> 'CharBuffer': ...
    @typing.overload
    @staticmethod
    def wrap(charArray: typing.Union[typing.List[str], jpype.JArray], int: int, int2: int) -> 'CharBuffer': ...
    @typing.overload
    @staticmethod
    def wrap(charSequence: typing.Union[java.lang.CharSequence, str]) -> 'CharBuffer': ...
    @typing.overload
    @staticmethod
    def wrap(charSequence: typing.Union[java.lang.CharSequence, str], int: int, int2: int) -> 'CharBuffer': ...

class DoubleBuffer(Buffer, java.lang.Comparable['DoubleBuffer']):
    @staticmethod
    def allocate(int: int) -> 'DoubleBuffer': ...
    def array(self) -> typing.MutableSequence[float]: ...
    def arrayOffset(self) -> int: ...
    def asReadOnlyBuffer(self) -> 'DoubleBuffer': ...
    def clear(self) -> 'DoubleBuffer': ...
    def compact(self) -> 'DoubleBuffer': ...
    def compareTo(self, doubleBuffer: 'DoubleBuffer') -> int: ...
    def duplicate(self) -> 'DoubleBuffer': ...
    def equals(self, object: typing.Any) -> bool: ...
    def flip(self) -> 'DoubleBuffer': ...
    @typing.overload
    def get(self) -> float: ...
    @typing.overload
    def get(self, int: int) -> float: ...
    @typing.overload
    def get(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> 'DoubleBuffer': ...
    @typing.overload
    def get(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> 'DoubleBuffer': ...
    @typing.overload
    def get(self, int: int, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> 'DoubleBuffer': ...
    @typing.overload
    def get(self, int: int, doubleArray: typing.Union[typing.List[float], jpype.JArray], int2: int, int3: int) -> 'DoubleBuffer': ...
    def hasArray(self) -> bool: ...
    def hashCode(self) -> int: ...
    def isDirect(self) -> bool: ...
    @typing.overload
    def limit(self) -> int: ...
    @typing.overload
    def limit(self, int: int) -> 'DoubleBuffer': ...
    def mark(self) -> 'DoubleBuffer': ...
    def mismatch(self, doubleBuffer: 'DoubleBuffer') -> int: ...
    def order(self) -> ByteOrder: ...
    @typing.overload
    def position(self) -> int: ...
    @typing.overload
    def position(self, int: int) -> 'DoubleBuffer': ...
    @typing.overload
    def put(self, double: float) -> 'DoubleBuffer': ...
    @typing.overload
    def put(self, int: int, double: float) -> 'DoubleBuffer': ...
    @typing.overload
    def put(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> 'DoubleBuffer': ...
    @typing.overload
    def put(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> 'DoubleBuffer': ...
    @typing.overload
    def put(self, int: int, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> 'DoubleBuffer': ...
    @typing.overload
    def put(self, int: int, doubleArray: typing.Union[typing.List[float], jpype.JArray], int2: int, int3: int) -> 'DoubleBuffer': ...
    @typing.overload
    def put(self, int: int, doubleBuffer: 'DoubleBuffer', int2: int, int3: int) -> 'DoubleBuffer': ...
    @typing.overload
    def put(self, doubleBuffer: 'DoubleBuffer') -> 'DoubleBuffer': ...
    def reset(self) -> 'DoubleBuffer': ...
    def rewind(self) -> 'DoubleBuffer': ...
    @typing.overload
    def slice(self) -> 'DoubleBuffer': ...
    @typing.overload
    def slice(self, int: int, int2: int) -> 'DoubleBuffer': ...
    def toString(self) -> str: ...
    @typing.overload
    @staticmethod
    def wrap(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> 'DoubleBuffer': ...
    @typing.overload
    @staticmethod
    def wrap(doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> 'DoubleBuffer': ...

class FloatBuffer(Buffer, java.lang.Comparable['FloatBuffer']):
    @staticmethod
    def allocate(int: int) -> 'FloatBuffer': ...
    def array(self) -> typing.MutableSequence[float]: ...
    def arrayOffset(self) -> int: ...
    def asReadOnlyBuffer(self) -> 'FloatBuffer': ...
    def clear(self) -> 'FloatBuffer': ...
    def compact(self) -> 'FloatBuffer': ...
    def compareTo(self, floatBuffer: 'FloatBuffer') -> int: ...
    def duplicate(self) -> 'FloatBuffer': ...
    def equals(self, object: typing.Any) -> bool: ...
    def flip(self) -> 'FloatBuffer': ...
    @typing.overload
    def get(self) -> float: ...
    @typing.overload
    def get(self, int: int) -> float: ...
    @typing.overload
    def get(self, floatArray: typing.Union[typing.List[float], jpype.JArray]) -> 'FloatBuffer': ...
    @typing.overload
    def get(self, floatArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> 'FloatBuffer': ...
    @typing.overload
    def get(self, int: int, floatArray: typing.Union[typing.List[float], jpype.JArray]) -> 'FloatBuffer': ...
    @typing.overload
    def get(self, int: int, floatArray: typing.Union[typing.List[float], jpype.JArray], int2: int, int3: int) -> 'FloatBuffer': ...
    def hasArray(self) -> bool: ...
    def hashCode(self) -> int: ...
    def isDirect(self) -> bool: ...
    @typing.overload
    def limit(self) -> int: ...
    @typing.overload
    def limit(self, int: int) -> 'FloatBuffer': ...
    def mark(self) -> 'FloatBuffer': ...
    def mismatch(self, floatBuffer: 'FloatBuffer') -> int: ...
    def order(self) -> ByteOrder: ...
    @typing.overload
    def position(self) -> int: ...
    @typing.overload
    def position(self, int: int) -> 'FloatBuffer': ...
    @typing.overload
    def put(self, float: float) -> 'FloatBuffer': ...
    @typing.overload
    def put(self, int: int, float: float) -> 'FloatBuffer': ...
    @typing.overload
    def put(self, floatArray: typing.Union[typing.List[float], jpype.JArray]) -> 'FloatBuffer': ...
    @typing.overload
    def put(self, floatArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> 'FloatBuffer': ...
    @typing.overload
    def put(self, int: int, floatArray: typing.Union[typing.List[float], jpype.JArray]) -> 'FloatBuffer': ...
    @typing.overload
    def put(self, int: int, floatArray: typing.Union[typing.List[float], jpype.JArray], int2: int, int3: int) -> 'FloatBuffer': ...
    @typing.overload
    def put(self, int: int, floatBuffer: 'FloatBuffer', int2: int, int3: int) -> 'FloatBuffer': ...
    @typing.overload
    def put(self, floatBuffer: 'FloatBuffer') -> 'FloatBuffer': ...
    def reset(self) -> 'FloatBuffer': ...
    def rewind(self) -> 'FloatBuffer': ...
    @typing.overload
    def slice(self) -> 'FloatBuffer': ...
    @typing.overload
    def slice(self, int: int, int2: int) -> 'FloatBuffer': ...
    def toString(self) -> str: ...
    @typing.overload
    @staticmethod
    def wrap(floatArray: typing.Union[typing.List[float], jpype.JArray]) -> 'FloatBuffer': ...
    @typing.overload
    @staticmethod
    def wrap(floatArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> 'FloatBuffer': ...

class IntBuffer(Buffer, java.lang.Comparable['IntBuffer']):
    @staticmethod
    def allocate(int: int) -> 'IntBuffer': ...
    def array(self) -> typing.MutableSequence[int]: ...
    def arrayOffset(self) -> int: ...
    def asReadOnlyBuffer(self) -> 'IntBuffer': ...
    def clear(self) -> 'IntBuffer': ...
    def compact(self) -> 'IntBuffer': ...
    def compareTo(self, intBuffer: 'IntBuffer') -> int: ...
    def duplicate(self) -> 'IntBuffer': ...
    def equals(self, object: typing.Any) -> bool: ...
    def flip(self) -> 'IntBuffer': ...
    @typing.overload
    def get(self) -> int: ...
    @typing.overload
    def get(self, int: int) -> int: ...
    @typing.overload
    def get(self, int: int, intArray: typing.Union[typing.List[int], jpype.JArray]) -> 'IntBuffer': ...
    @typing.overload
    def get(self, int: int, intArray: typing.Union[typing.List[int], jpype.JArray], int3: int, int4: int) -> 'IntBuffer': ...
    @typing.overload
    def get(self, intArray: typing.Union[typing.List[int], jpype.JArray]) -> 'IntBuffer': ...
    @typing.overload
    def get(self, intArray: typing.Union[typing.List[int], jpype.JArray], int2: int, int3: int) -> 'IntBuffer': ...
    def hasArray(self) -> bool: ...
    def hashCode(self) -> int: ...
    def isDirect(self) -> bool: ...
    @typing.overload
    def limit(self) -> int: ...
    @typing.overload
    def limit(self, int: int) -> 'IntBuffer': ...
    def mark(self) -> 'IntBuffer': ...
    def mismatch(self, intBuffer: 'IntBuffer') -> int: ...
    def order(self) -> ByteOrder: ...
    @typing.overload
    def position(self) -> int: ...
    @typing.overload
    def position(self, int: int) -> 'IntBuffer': ...
    @typing.overload
    def put(self, int: int) -> 'IntBuffer': ...
    @typing.overload
    def put(self, int: int, int2: int) -> 'IntBuffer': ...
    @typing.overload
    def put(self, intArray: typing.Union[typing.List[int], jpype.JArray]) -> 'IntBuffer': ...
    @typing.overload
    def put(self, int: int, intArray: typing.Union[typing.List[int], jpype.JArray]) -> 'IntBuffer': ...
    @typing.overload
    def put(self, int: int, intArray: typing.Union[typing.List[int], jpype.JArray], int3: int, int4: int) -> 'IntBuffer': ...
    @typing.overload
    def put(self, int: int, intBuffer: 'IntBuffer', int3: int, int4: int) -> 'IntBuffer': ...
    @typing.overload
    def put(self, intArray: typing.Union[typing.List[int], jpype.JArray], int2: int, int3: int) -> 'IntBuffer': ...
    @typing.overload
    def put(self, intBuffer: 'IntBuffer') -> 'IntBuffer': ...
    def reset(self) -> 'IntBuffer': ...
    def rewind(self) -> 'IntBuffer': ...
    @typing.overload
    def slice(self) -> 'IntBuffer': ...
    @typing.overload
    def slice(self, int: int, int2: int) -> 'IntBuffer': ...
    def toString(self) -> str: ...
    @typing.overload
    @staticmethod
    def wrap(intArray: typing.Union[typing.List[int], jpype.JArray]) -> 'IntBuffer': ...
    @typing.overload
    @staticmethod
    def wrap(intArray: typing.Union[typing.List[int], jpype.JArray], int2: int, int3: int) -> 'IntBuffer': ...

class LongBuffer(Buffer, java.lang.Comparable['LongBuffer']):
    @staticmethod
    def allocate(int: int) -> 'LongBuffer': ...
    def array(self) -> typing.MutableSequence[int]: ...
    def arrayOffset(self) -> int: ...
    def asReadOnlyBuffer(self) -> 'LongBuffer': ...
    def clear(self) -> 'LongBuffer': ...
    def compact(self) -> 'LongBuffer': ...
    def compareTo(self, longBuffer: 'LongBuffer') -> int: ...
    def duplicate(self) -> 'LongBuffer': ...
    def equals(self, object: typing.Any) -> bool: ...
    def flip(self) -> 'LongBuffer': ...
    @typing.overload
    def get(self) -> int: ...
    @typing.overload
    def get(self, int: int) -> int: ...
    @typing.overload
    def get(self, int: int, longArray: typing.Union[typing.List[int], jpype.JArray]) -> 'LongBuffer': ...
    @typing.overload
    def get(self, int: int, longArray: typing.Union[typing.List[int], jpype.JArray], int2: int, int3: int) -> 'LongBuffer': ...
    @typing.overload
    def get(self, longArray: typing.Union[typing.List[int], jpype.JArray]) -> 'LongBuffer': ...
    @typing.overload
    def get(self, longArray: typing.Union[typing.List[int], jpype.JArray], int: int, int2: int) -> 'LongBuffer': ...
    def hasArray(self) -> bool: ...
    def hashCode(self) -> int: ...
    def isDirect(self) -> bool: ...
    @typing.overload
    def limit(self) -> int: ...
    @typing.overload
    def limit(self, int: int) -> 'LongBuffer': ...
    def mark(self) -> 'LongBuffer': ...
    def mismatch(self, longBuffer: 'LongBuffer') -> int: ...
    def order(self) -> ByteOrder: ...
    @typing.overload
    def position(self) -> int: ...
    @typing.overload
    def position(self, int: int) -> 'LongBuffer': ...
    @typing.overload
    def put(self, int: int, long: int) -> 'LongBuffer': ...
    @typing.overload
    def put(self, long: int) -> 'LongBuffer': ...
    @typing.overload
    def put(self, longArray: typing.Union[typing.List[int], jpype.JArray]) -> 'LongBuffer': ...
    @typing.overload
    def put(self, int: int, longBuffer: 'LongBuffer', int2: int, int3: int) -> 'LongBuffer': ...
    @typing.overload
    def put(self, int: int, longArray: typing.Union[typing.List[int], jpype.JArray]) -> 'LongBuffer': ...
    @typing.overload
    def put(self, int: int, longArray: typing.Union[typing.List[int], jpype.JArray], int2: int, int3: int) -> 'LongBuffer': ...
    @typing.overload
    def put(self, longBuffer: 'LongBuffer') -> 'LongBuffer': ...
    @typing.overload
    def put(self, longArray: typing.Union[typing.List[int], jpype.JArray], int: int, int2: int) -> 'LongBuffer': ...
    def reset(self) -> 'LongBuffer': ...
    def rewind(self) -> 'LongBuffer': ...
    @typing.overload
    def slice(self) -> 'LongBuffer': ...
    @typing.overload
    def slice(self, int: int, int2: int) -> 'LongBuffer': ...
    def toString(self) -> str: ...
    @typing.overload
    @staticmethod
    def wrap(longArray: typing.Union[typing.List[int], jpype.JArray]) -> 'LongBuffer': ...
    @typing.overload
    @staticmethod
    def wrap(longArray: typing.Union[typing.List[int], jpype.JArray], int: int, int2: int) -> 'LongBuffer': ...

class ShortBuffer(Buffer, java.lang.Comparable['ShortBuffer']):
    @staticmethod
    def allocate(int: int) -> 'ShortBuffer': ...
    def array(self) -> typing.MutableSequence[int]: ...
    def arrayOffset(self) -> int: ...
    def asReadOnlyBuffer(self) -> 'ShortBuffer': ...
    def clear(self) -> 'ShortBuffer': ...
    def compact(self) -> 'ShortBuffer': ...
    def compareTo(self, shortBuffer: 'ShortBuffer') -> int: ...
    def duplicate(self) -> 'ShortBuffer': ...
    def equals(self, object: typing.Any) -> bool: ...
    def flip(self) -> 'ShortBuffer': ...
    @typing.overload
    def get(self) -> int: ...
    @typing.overload
    def get(self, int: int) -> int: ...
    @typing.overload
    def get(self, int: int, shortArray: typing.Union[typing.List[int], jpype.JArray]) -> 'ShortBuffer': ...
    @typing.overload
    def get(self, int: int, shortArray: typing.Union[typing.List[int], jpype.JArray], int2: int, int3: int) -> 'ShortBuffer': ...
    @typing.overload
    def get(self, shortArray: typing.Union[typing.List[int], jpype.JArray]) -> 'ShortBuffer': ...
    @typing.overload
    def get(self, shortArray: typing.Union[typing.List[int], jpype.JArray], int: int, int2: int) -> 'ShortBuffer': ...
    def hasArray(self) -> bool: ...
    def hashCode(self) -> int: ...
    def isDirect(self) -> bool: ...
    @typing.overload
    def limit(self) -> int: ...
    @typing.overload
    def limit(self, int: int) -> 'ShortBuffer': ...
    def mark(self) -> 'ShortBuffer': ...
    def mismatch(self, shortBuffer: 'ShortBuffer') -> int: ...
    def order(self) -> ByteOrder: ...
    @typing.overload
    def position(self) -> int: ...
    @typing.overload
    def position(self, int: int) -> 'ShortBuffer': ...
    @typing.overload
    def put(self, int: int, short: int) -> 'ShortBuffer': ...
    @typing.overload
    def put(self, short: int) -> 'ShortBuffer': ...
    @typing.overload
    def put(self, shortArray: typing.Union[typing.List[int], jpype.JArray]) -> 'ShortBuffer': ...
    @typing.overload
    def put(self, int: int, shortBuffer: 'ShortBuffer', int2: int, int3: int) -> 'ShortBuffer': ...
    @typing.overload
    def put(self, int: int, shortArray: typing.Union[typing.List[int], jpype.JArray]) -> 'ShortBuffer': ...
    @typing.overload
    def put(self, int: int, shortArray: typing.Union[typing.List[int], jpype.JArray], int2: int, int3: int) -> 'ShortBuffer': ...
    @typing.overload
    def put(self, shortBuffer: 'ShortBuffer') -> 'ShortBuffer': ...
    @typing.overload
    def put(self, shortArray: typing.Union[typing.List[int], jpype.JArray], int: int, int2: int) -> 'ShortBuffer': ...
    def reset(self) -> 'ShortBuffer': ...
    def rewind(self) -> 'ShortBuffer': ...
    @typing.overload
    def slice(self) -> 'ShortBuffer': ...
    @typing.overload
    def slice(self, int: int, int2: int) -> 'ShortBuffer': ...
    def toString(self) -> str: ...
    @typing.overload
    @staticmethod
    def wrap(shortArray: typing.Union[typing.List[int], jpype.JArray]) -> 'ShortBuffer': ...
    @typing.overload
    @staticmethod
    def wrap(shortArray: typing.Union[typing.List[int], jpype.JArray], int: int, int2: int) -> 'ShortBuffer': ...

class MappedByteBuffer(ByteBuffer):
    def clear(self) -> 'MappedByteBuffer': ...
    def compact(self) -> 'MappedByteBuffer': ...
    def duplicate(self) -> 'MappedByteBuffer': ...
    def flip(self) -> 'MappedByteBuffer': ...
    @typing.overload
    def force(self) -> 'MappedByteBuffer': ...
    @typing.overload
    def force(self, int: int, int2: int) -> 'MappedByteBuffer': ...
    def isLoaded(self) -> bool: ...
    @typing.overload
    def limit(self) -> int: ...
    @typing.overload
    def limit(self, int: int) -> 'MappedByteBuffer': ...
    def load(self) -> 'MappedByteBuffer': ...
    def mark(self) -> 'MappedByteBuffer': ...
    @typing.overload
    def position(self) -> int: ...
    @typing.overload
    def position(self, int: int) -> 'MappedByteBuffer': ...
    def reset(self) -> 'MappedByteBuffer': ...
    def rewind(self) -> 'MappedByteBuffer': ...
    @typing.overload
    def slice(self) -> 'MappedByteBuffer': ...
    @typing.overload
    def slice(self, int: int, int2: int) -> 'MappedByteBuffer': ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("java.nio")``.

    Buffer: typing.Type[Buffer]
    BufferOverflowException: typing.Type[BufferOverflowException]
    BufferUnderflowException: typing.Type[BufferUnderflowException]
    ByteBuffer: typing.Type[ByteBuffer]
    ByteOrder: typing.Type[ByteOrder]
    CharBuffer: typing.Type[CharBuffer]
    DoubleBuffer: typing.Type[DoubleBuffer]
    FloatBuffer: typing.Type[FloatBuffer]
    IntBuffer: typing.Type[IntBuffer]
    InvalidMarkException: typing.Type[InvalidMarkException]
    LongBuffer: typing.Type[LongBuffer]
    MappedByteBuffer: typing.Type[MappedByteBuffer]
    ReadOnlyBufferException: typing.Type[ReadOnlyBufferException]
    ShortBuffer: typing.Type[ShortBuffer]
    channels: java.nio.channels.__module_protocol__
    charset: java.nio.charset.__module_protocol__
    file: java.nio.file.__module_protocol__
