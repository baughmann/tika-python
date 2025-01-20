
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import datetime
import java.io
import java.lang
import java.security
import java.time
import java.util
import java.util.function
import jpype
import typing



class ErrorManager:
    GENERIC_FAILURE: typing.ClassVar[int] = ...
    WRITE_FAILURE: typing.ClassVar[int] = ...
    FLUSH_FAILURE: typing.ClassVar[int] = ...
    CLOSE_FAILURE: typing.ClassVar[int] = ...
    OPEN_FAILURE: typing.ClassVar[int] = ...
    FORMAT_FAILURE: typing.ClassVar[int] = ...
    def __init__(self): ...
    def error(self, string: str, exception: java.lang.Exception, int: int) -> None: ...

class Filter:
    def isLoggable(self, logRecord: 'LogRecord') -> bool: ...

class Formatter:
    def format(self, logRecord: 'LogRecord') -> str: ...
    def formatMessage(self, logRecord: 'LogRecord') -> str: ...
    def getHead(self, handler: 'Handler') -> str: ...
    def getTail(self, handler: 'Handler') -> str: ...

class Handler:
    def close(self) -> None: ...
    def flush(self) -> None: ...
    def getEncoding(self) -> str: ...
    def getErrorManager(self) -> ErrorManager: ...
    def getFilter(self) -> Filter: ...
    def getFormatter(self) -> Formatter: ...
    def getLevel(self) -> 'Level': ...
    def isLoggable(self, logRecord: 'LogRecord') -> bool: ...
    def publish(self, logRecord: 'LogRecord') -> None: ...
    def setEncoding(self, string: str) -> None: ...
    def setErrorManager(self, errorManager: ErrorManager) -> None: ...
    def setFilter(self, filter: typing.Union[Filter, typing.Callable]) -> None: ...
    def setFormatter(self, formatter: Formatter) -> None: ...
    def setLevel(self, level: 'Level') -> None: ...

class Level(java.io.Serializable):
    OFF: typing.ClassVar['Level'] = ...
    SEVERE: typing.ClassVar['Level'] = ...
    WARNING: typing.ClassVar['Level'] = ...
    INFO: typing.ClassVar['Level'] = ...
    CONFIG: typing.ClassVar['Level'] = ...
    FINE: typing.ClassVar['Level'] = ...
    FINER: typing.ClassVar['Level'] = ...
    FINEST: typing.ClassVar['Level'] = ...
    ALL: typing.ClassVar['Level'] = ...
    def equals(self, object: typing.Any) -> bool: ...
    def getLocalizedName(self) -> str: ...
    def getName(self) -> str: ...
    def getResourceBundleName(self) -> str: ...
    def hashCode(self) -> int: ...
    def intValue(self) -> int: ...
    @staticmethod
    def parse(string: str) -> 'Level': ...
    def toString(self) -> str: ...

class LogManager:
    LOGGING_MXBEAN_NAME: typing.ClassVar[str] = ...
    def addConfigurationListener(self, runnable: typing.Union[java.lang.Runnable, typing.Callable]) -> 'LogManager': ...
    def addLogger(self, logger: 'Logger') -> bool: ...
    def checkAccess(self) -> None: ...
    @staticmethod
    def getLogManager() -> 'LogManager': ...
    def getLogger(self, string: str) -> 'Logger': ...
    def getLoggerNames(self) -> java.util.Enumeration[str]: ...
    @staticmethod
    def getLoggingMXBean() -> 'LoggingMXBean': ...
    def getProperty(self, string: str) -> str: ...
    @typing.overload
    def readConfiguration(self) -> None: ...
    @typing.overload
    def readConfiguration(self, inputStream: java.io.InputStream) -> None: ...
    def removeConfigurationListener(self, runnable: typing.Union[java.lang.Runnable, typing.Callable]) -> None: ...
    def reset(self) -> None: ...
    @typing.overload
    def updateConfiguration(self, inputStream: java.io.InputStream, function: typing.Union[java.util.function.Function[str, typing.Union[java.util.function.BiFunction[str, str, str], typing.Callable[[str, str], str]]], typing.Callable[[str], typing.Union[java.util.function.BiFunction[str, str, str], typing.Callable[[str, str], str]]]]) -> None: ...
    @typing.overload
    def updateConfiguration(self, function: typing.Union[java.util.function.Function[str, typing.Union[java.util.function.BiFunction[str, str, str], typing.Callable[[str, str], str]]], typing.Callable[[str], typing.Union[java.util.function.BiFunction[str, str, str], typing.Callable[[str, str], str]]]]) -> None: ...

class LogRecord(java.io.Serializable):
    def __init__(self, level: Level, string: str): ...
    def getInstant(self) -> java.time.Instant: ...
    def getLevel(self) -> Level: ...
    def getLoggerName(self) -> str: ...
    def getLongThreadID(self) -> int: ...
    def getMessage(self) -> str: ...
    def getMillis(self) -> int: ...
    def getParameters(self) -> typing.MutableSequence[typing.Any]: ...
    def getResourceBundle(self) -> java.util.ResourceBundle: ...
    def getResourceBundleName(self) -> str: ...
    def getSequenceNumber(self) -> int: ...
    def getSourceClassName(self) -> str: ...
    def getSourceMethodName(self) -> str: ...
    def getThreadID(self) -> int: ...
    def getThrown(self) -> java.lang.Throwable: ...
    def setInstant(self, instant: typing.Union[java.time.Instant, datetime.datetime]) -> None: ...
    def setLevel(self, level: Level) -> None: ...
    def setLoggerName(self, string: str) -> None: ...
    def setLongThreadID(self, long: int) -> 'LogRecord': ...
    def setMessage(self, string: str) -> None: ...
    def setMillis(self, long: int) -> None: ...
    def setParameters(self, objectArray: typing.Union[typing.List[typing.Any], jpype.JArray]) -> None: ...
    def setResourceBundle(self, resourceBundle: java.util.ResourceBundle) -> None: ...
    def setResourceBundleName(self, string: str) -> None: ...
    def setSequenceNumber(self, long: int) -> None: ...
    def setSourceClassName(self, string: str) -> None: ...
    def setSourceMethodName(self, string: str) -> None: ...
    def setThreadID(self, int: int) -> None: ...
    def setThrown(self, throwable: java.lang.Throwable) -> None: ...

class Logger:
    GLOBAL_LOGGER_NAME: typing.ClassVar[str] = ...
    global_: typing.ClassVar['Logger'] = ...
    def addHandler(self, handler: Handler) -> None: ...
    @typing.overload
    def config(self, string: str) -> None: ...
    @typing.overload
    def config(self, supplier: typing.Union[java.util.function.Supplier[str], typing.Callable[[], str]]) -> None: ...
    @typing.overload
    def entering(self, string: str, string2: str) -> None: ...
    @typing.overload
    def entering(self, string: str, string2: str, object: typing.Any) -> None: ...
    @typing.overload
    def entering(self, string: str, string2: str, objectArray: typing.Union[typing.List[typing.Any], jpype.JArray]) -> None: ...
    @typing.overload
    def exiting(self, string: str, string2: str) -> None: ...
    @typing.overload
    def exiting(self, string: str, string2: str, object: typing.Any) -> None: ...
    @typing.overload
    def fine(self, string: str) -> None: ...
    @typing.overload
    def fine(self, supplier: typing.Union[java.util.function.Supplier[str], typing.Callable[[], str]]) -> None: ...
    @typing.overload
    def finer(self, string: str) -> None: ...
    @typing.overload
    def finer(self, supplier: typing.Union[java.util.function.Supplier[str], typing.Callable[[], str]]) -> None: ...
    @typing.overload
    def finest(self, string: str) -> None: ...
    @typing.overload
    def finest(self, supplier: typing.Union[java.util.function.Supplier[str], typing.Callable[[], str]]) -> None: ...
    @typing.overload
    @staticmethod
    def getAnonymousLogger() -> 'Logger': ...
    @typing.overload
    @staticmethod
    def getAnonymousLogger(string: str) -> 'Logger': ...
    def getFilter(self) -> Filter: ...
    @staticmethod
    def getGlobal() -> 'Logger': ...
    def getHandlers(self) -> typing.MutableSequence[Handler]: ...
    def getLevel(self) -> Level: ...
    @typing.overload
    @staticmethod
    def getLogger(string: str) -> 'Logger': ...
    @typing.overload
    @staticmethod
    def getLogger(string: str, string2: str) -> 'Logger': ...
    def getName(self) -> str: ...
    def getParent(self) -> 'Logger': ...
    def getResourceBundle(self) -> java.util.ResourceBundle: ...
    def getResourceBundleName(self) -> str: ...
    def getUseParentHandlers(self) -> bool: ...
    @typing.overload
    def info(self, string: str) -> None: ...
    @typing.overload
    def info(self, supplier: typing.Union[java.util.function.Supplier[str], typing.Callable[[], str]]) -> None: ...
    def isLoggable(self, level: Level) -> bool: ...
    @typing.overload
    def log(self, level: Level, string: str) -> None: ...
    @typing.overload
    def log(self, level: Level, string: str, object: typing.Any) -> None: ...
    @typing.overload
    def log(self, level: Level, string: str, objectArray: typing.Union[typing.List[typing.Any], jpype.JArray]) -> None: ...
    @typing.overload
    def log(self, level: Level, string: str, throwable: java.lang.Throwable) -> None: ...
    @typing.overload
    def log(self, level: Level, throwable: java.lang.Throwable, supplier: typing.Union[java.util.function.Supplier[str], typing.Callable[[], str]]) -> None: ...
    @typing.overload
    def log(self, level: Level, supplier: typing.Union[java.util.function.Supplier[str], typing.Callable[[], str]]) -> None: ...
    @typing.overload
    def log(self, logRecord: LogRecord) -> None: ...
    @typing.overload
    def logp(self, level: Level, string: str, string2: str, string3: str) -> None: ...
    @typing.overload
    def logp(self, level: Level, string: str, string2: str, string3: str, object: typing.Any) -> None: ...
    @typing.overload
    def logp(self, level: Level, string: str, string2: str, string3: str, objectArray: typing.Union[typing.List[typing.Any], jpype.JArray]) -> None: ...
    @typing.overload
    def logp(self, level: Level, string: str, string2: str, string3: str, throwable: java.lang.Throwable) -> None: ...
    @typing.overload
    def logp(self, level: Level, string: str, string2: str, throwable: java.lang.Throwable, supplier: typing.Union[java.util.function.Supplier[str], typing.Callable[[], str]]) -> None: ...
    @typing.overload
    def logp(self, level: Level, string: str, string2: str, supplier: typing.Union[java.util.function.Supplier[str], typing.Callable[[], str]]) -> None: ...
    @typing.overload
    def logrb(self, level: Level, string: str, string2: str, string3: str, string4: str) -> None: ...
    @typing.overload
    def logrb(self, level: Level, string: str, string2: str, string3: str, string4: str, object: typing.Any) -> None: ...
    @typing.overload
    def logrb(self, level: Level, string: str, string2: str, string3: str, string4: str, objectArray: typing.Union[typing.List[typing.Any], jpype.JArray]) -> None: ...
    @typing.overload
    def logrb(self, level: Level, string: str, string2: str, string3: str, string4: str, throwable: java.lang.Throwable) -> None: ...
    @typing.overload
    def logrb(self, level: Level, string: str, string2: str, resourceBundle: java.util.ResourceBundle, string3: str, *object: typing.Any) -> None: ...
    @typing.overload
    def logrb(self, level: Level, string: str, string2: str, resourceBundle: java.util.ResourceBundle, string3: str, throwable: java.lang.Throwable) -> None: ...
    @typing.overload
    def logrb(self, level: Level, resourceBundle: java.util.ResourceBundle, string: str, *object: typing.Any) -> None: ...
    @typing.overload
    def logrb(self, level: Level, resourceBundle: java.util.ResourceBundle, string: str, throwable: java.lang.Throwable) -> None: ...
    def removeHandler(self, handler: Handler) -> None: ...
    def setFilter(self, filter: typing.Union[Filter, typing.Callable]) -> None: ...
    def setLevel(self, level: Level) -> None: ...
    def setParent(self, logger: 'Logger') -> None: ...
    def setResourceBundle(self, resourceBundle: java.util.ResourceBundle) -> None: ...
    def setUseParentHandlers(self, boolean: bool) -> None: ...
    @typing.overload
    def severe(self, string: str) -> None: ...
    @typing.overload
    def severe(self, supplier: typing.Union[java.util.function.Supplier[str], typing.Callable[[], str]]) -> None: ...
    def throwing(self, string: str, string2: str, throwable: java.lang.Throwable) -> None: ...
    @typing.overload
    def warning(self, string: str) -> None: ...
    @typing.overload
    def warning(self, supplier: typing.Union[java.util.function.Supplier[str], typing.Callable[[], str]]) -> None: ...

class LoggingMXBean:
    def getLoggerLevel(self, string: str) -> str: ...
    def getLoggerNames(self) -> java.util.List[str]: ...
    def getParentLoggerName(self, string: str) -> str: ...
    def setLoggerLevel(self, string: str, string2: str) -> None: ...

class LoggingPermission(java.security.BasicPermission):
    def __init__(self, string: str, string2: str): ...

class MemoryHandler(Handler):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, handler: Handler, int: int, level: Level): ...
    def close(self) -> None: ...
    def flush(self) -> None: ...
    def getPushLevel(self) -> Level: ...
    def isLoggable(self, logRecord: LogRecord) -> bool: ...
    def publish(self, logRecord: LogRecord) -> None: ...
    def push(self) -> None: ...
    def setPushLevel(self, level: Level) -> None: ...

class SimpleFormatter(Formatter):
    def __init__(self): ...
    def format(self, logRecord: LogRecord) -> str: ...

class StreamHandler(Handler):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, outputStream: java.io.OutputStream, formatter: Formatter): ...
    def close(self) -> None: ...
    def flush(self) -> None: ...
    def isLoggable(self, logRecord: LogRecord) -> bool: ...
    def publish(self, logRecord: LogRecord) -> None: ...
    def setEncoding(self, string: str) -> None: ...

class XMLFormatter(Formatter):
    def __init__(self): ...
    def format(self, logRecord: LogRecord) -> str: ...
    def getHead(self, handler: Handler) -> str: ...
    def getTail(self, handler: Handler) -> str: ...

class ConsoleHandler(StreamHandler):
    def __init__(self): ...
    def close(self) -> None: ...
    def publish(self, logRecord: LogRecord) -> None: ...

class FileHandler(StreamHandler):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def __init__(self, string: str, boolean: bool): ...
    @typing.overload
    def __init__(self, string: str, int: int, int2: int): ...
    @typing.overload
    def __init__(self, string: str, int: int, int2: int, boolean: bool): ...
    @typing.overload
    def __init__(self, string: str, long: int, int: int, boolean: bool): ...
    def close(self) -> None: ...
    def publish(self, logRecord: LogRecord) -> None: ...

class SocketHandler(StreamHandler):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: str, int: int): ...
    def close(self) -> None: ...
    def publish(self, logRecord: LogRecord) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("java.util.logging")``.

    ConsoleHandler: typing.Type[ConsoleHandler]
    ErrorManager: typing.Type[ErrorManager]
    FileHandler: typing.Type[FileHandler]
    Filter: typing.Type[Filter]
    Formatter: typing.Type[Formatter]
    Handler: typing.Type[Handler]
    Level: typing.Type[Level]
    LogManager: typing.Type[LogManager]
    LogRecord: typing.Type[LogRecord]
    Logger: typing.Type[Logger]
    LoggingMXBean: typing.Type[LoggingMXBean]
    LoggingPermission: typing.Type[LoggingPermission]
    MemoryHandler: typing.Type[MemoryHandler]
    SimpleFormatter: typing.Type[SimpleFormatter]
    SocketHandler: typing.Type[SocketHandler]
    StreamHandler: typing.Type[StreamHandler]
    XMLFormatter: typing.Type[XMLFormatter]
