
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import java.security
import java.util
import javax.management
import javax.management.openmbean
import jpype
import typing



class LockInfo:
    def __init__(self, string: str, int: int): ...
    @staticmethod
    def from_(compositeData: javax.management.openmbean.CompositeData) -> 'LockInfo': ...
    def getClassName(self) -> str: ...
    def getIdentityHashCode(self) -> int: ...
    def toString(self) -> str: ...

class ManagementFactory:
    CLASS_LOADING_MXBEAN_NAME: typing.ClassVar[str] = ...
    COMPILATION_MXBEAN_NAME: typing.ClassVar[str] = ...
    MEMORY_MXBEAN_NAME: typing.ClassVar[str] = ...
    OPERATING_SYSTEM_MXBEAN_NAME: typing.ClassVar[str] = ...
    RUNTIME_MXBEAN_NAME: typing.ClassVar[str] = ...
    THREAD_MXBEAN_NAME: typing.ClassVar[str] = ...
    GARBAGE_COLLECTOR_MXBEAN_DOMAIN_TYPE: typing.ClassVar[str] = ...
    MEMORY_MANAGER_MXBEAN_DOMAIN_TYPE: typing.ClassVar[str] = ...
    MEMORY_POOL_MXBEAN_DOMAIN_TYPE: typing.ClassVar[str] = ...
    @staticmethod
    def getClassLoadingMXBean() -> 'ClassLoadingMXBean': ...
    @staticmethod
    def getCompilationMXBean() -> 'CompilationMXBean': ...
    @staticmethod
    def getGarbageCollectorMXBeans() -> java.util.List['GarbageCollectorMXBean']: ...
    @staticmethod
    def getMemoryMXBean() -> 'MemoryMXBean': ...
    @staticmethod
    def getMemoryManagerMXBeans() -> java.util.List['MemoryManagerMXBean']: ...
    @staticmethod
    def getMemoryPoolMXBeans() -> java.util.List['MemoryPoolMXBean']: ...
    @staticmethod
    def getOperatingSystemMXBean() -> 'OperatingSystemMXBean': ...
    @staticmethod
    def getPlatformMBeanServer() -> javax.management.MBeanServer: ...
    _getPlatformMXBean_0__T = typing.TypeVar('_getPlatformMXBean_0__T', bound='PlatformManagedObject')  # <T>
    _getPlatformMXBean_1__T = typing.TypeVar('_getPlatformMXBean_1__T', bound='PlatformManagedObject')  # <T>
    @typing.overload
    @staticmethod
    def getPlatformMXBean(class_: typing.Type[_getPlatformMXBean_0__T]) -> _getPlatformMXBean_0__T: ...
    @typing.overload
    @staticmethod
    def getPlatformMXBean(mBeanServerConnection: javax.management.MBeanServerConnection, class_: typing.Type[_getPlatformMXBean_1__T]) -> _getPlatformMXBean_1__T: ...
    _getPlatformMXBeans_0__T = typing.TypeVar('_getPlatformMXBeans_0__T', bound='PlatformManagedObject')  # <T>
    _getPlatformMXBeans_1__T = typing.TypeVar('_getPlatformMXBeans_1__T', bound='PlatformManagedObject')  # <T>
    @typing.overload
    @staticmethod
    def getPlatformMXBeans(class_: typing.Type[_getPlatformMXBeans_0__T]) -> java.util.List[_getPlatformMXBeans_0__T]: ...
    @typing.overload
    @staticmethod
    def getPlatformMXBeans(mBeanServerConnection: javax.management.MBeanServerConnection, class_: typing.Type[_getPlatformMXBeans_1__T]) -> java.util.List[_getPlatformMXBeans_1__T]: ...
    @staticmethod
    def getPlatformManagementInterfaces() -> java.util.Set[typing.Type['PlatformManagedObject']]: ...
    @staticmethod
    def getRuntimeMXBean() -> 'RuntimeMXBean': ...
    @staticmethod
    def getThreadMXBean() -> 'ThreadMXBean': ...
    _newPlatformMXBeanProxy__T = typing.TypeVar('_newPlatformMXBeanProxy__T')  # <T>
    @staticmethod
    def newPlatformMXBeanProxy(mBeanServerConnection: javax.management.MBeanServerConnection, string: str, class_: typing.Type[_newPlatformMXBeanProxy__T]) -> _newPlatformMXBeanProxy__T: ...

class ManagementPermission(java.security.BasicPermission):
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def __init__(self, string: str, string2: str): ...

class MemoryNotificationInfo:
    MEMORY_THRESHOLD_EXCEEDED: typing.ClassVar[str] = ...
    MEMORY_COLLECTION_THRESHOLD_EXCEEDED: typing.ClassVar[str] = ...
    def __init__(self, string: str, memoryUsage: 'MemoryUsage', long: int): ...
    @staticmethod
    def from_(compositeData: javax.management.openmbean.CompositeData) -> 'MemoryNotificationInfo': ...
    def getCount(self) -> int: ...
    def getPoolName(self) -> str: ...
    def getUsage(self) -> 'MemoryUsage': ...

class MemoryType(java.lang.Enum['MemoryType']):
    HEAP: typing.ClassVar['MemoryType'] = ...
    NON_HEAP: typing.ClassVar['MemoryType'] = ...
    def toString(self) -> str: ...
    _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'MemoryType': ...
    @staticmethod
    def values() -> typing.MutableSequence['MemoryType']: ...

class MemoryUsage:
    def __init__(self, long: int, long2: int, long3: int, long4: int): ...
    @staticmethod
    def from_(compositeData: javax.management.openmbean.CompositeData) -> 'MemoryUsage': ...
    def getCommitted(self) -> int: ...
    def getInit(self) -> int: ...
    def getMax(self) -> int: ...
    def getUsed(self) -> int: ...
    def toString(self) -> str: ...

class PlatformManagedObject:
    def getObjectName(self) -> javax.management.ObjectName: ...

class ThreadInfo:
    @staticmethod
    def from_(compositeData: javax.management.openmbean.CompositeData) -> 'ThreadInfo': ...
    def getBlockedCount(self) -> int: ...
    def getBlockedTime(self) -> int: ...
    def getLockInfo(self) -> LockInfo: ...
    def getLockName(self) -> str: ...
    def getLockOwnerId(self) -> int: ...
    def getLockOwnerName(self) -> str: ...
    def getLockedMonitors(self) -> typing.MutableSequence['MonitorInfo']: ...
    def getLockedSynchronizers(self) -> typing.MutableSequence[LockInfo]: ...
    def getPriority(self) -> int: ...
    def getStackTrace(self) -> typing.MutableSequence[java.lang.StackTraceElement]: ...
    def getThreadId(self) -> int: ...
    def getThreadName(self) -> str: ...
    def getThreadState(self) -> java.lang.Thread.State: ...
    def getWaitedCount(self) -> int: ...
    def getWaitedTime(self) -> int: ...
    def isDaemon(self) -> bool: ...
    def isInNative(self) -> bool: ...
    def isSuspended(self) -> bool: ...
    def toString(self) -> str: ...

class BufferPoolMXBean(PlatformManagedObject):
    def getCount(self) -> int: ...
    def getMemoryUsed(self) -> int: ...
    def getName(self) -> str: ...
    def getTotalCapacity(self) -> int: ...

class ClassLoadingMXBean(PlatformManagedObject):
    def getLoadedClassCount(self) -> int: ...
    def getTotalLoadedClassCount(self) -> int: ...
    def getUnloadedClassCount(self) -> int: ...
    def isVerbose(self) -> bool: ...
    def setVerbose(self, boolean: bool) -> None: ...

class CompilationMXBean(PlatformManagedObject):
    def getName(self) -> str: ...
    def getTotalCompilationTime(self) -> int: ...
    def isCompilationTimeMonitoringSupported(self) -> bool: ...

class MemoryMXBean(PlatformManagedObject):
    def gc(self) -> None: ...
    def getHeapMemoryUsage(self) -> MemoryUsage: ...
    def getNonHeapMemoryUsage(self) -> MemoryUsage: ...
    def getObjectPendingFinalizationCount(self) -> int: ...
    def isVerbose(self) -> bool: ...
    def setVerbose(self, boolean: bool) -> None: ...

class MemoryManagerMXBean(PlatformManagedObject):
    def getMemoryPoolNames(self) -> typing.MutableSequence[str]: ...
    def getName(self) -> str: ...
    def isValid(self) -> bool: ...

class MemoryPoolMXBean(PlatformManagedObject):
    def getCollectionUsage(self) -> MemoryUsage: ...
    def getCollectionUsageThreshold(self) -> int: ...
    def getCollectionUsageThresholdCount(self) -> int: ...
    def getMemoryManagerNames(self) -> typing.MutableSequence[str]: ...
    def getName(self) -> str: ...
    def getPeakUsage(self) -> MemoryUsage: ...
    def getType(self) -> MemoryType: ...
    def getUsage(self) -> MemoryUsage: ...
    def getUsageThreshold(self) -> int: ...
    def getUsageThresholdCount(self) -> int: ...
    def isCollectionUsageThresholdExceeded(self) -> bool: ...
    def isCollectionUsageThresholdSupported(self) -> bool: ...
    def isUsageThresholdExceeded(self) -> bool: ...
    def isUsageThresholdSupported(self) -> bool: ...
    def isValid(self) -> bool: ...
    def resetPeakUsage(self) -> None: ...
    def setCollectionUsageThreshold(self, long: int) -> None: ...
    def setUsageThreshold(self, long: int) -> None: ...

class MonitorInfo(LockInfo):
    def __init__(self, string: str, int: int, int2: int, stackTraceElement: java.lang.StackTraceElement): ...
    @typing.overload
    @staticmethod
    def from_(compositeData: javax.management.openmbean.CompositeData) -> LockInfo: ...
    @typing.overload
    @staticmethod
    def from_(compositeData: javax.management.openmbean.CompositeData) -> 'MonitorInfo': ...
    def getLockedStackDepth(self) -> int: ...
    def getLockedStackFrame(self) -> java.lang.StackTraceElement: ...

class OperatingSystemMXBean(PlatformManagedObject):
    def getArch(self) -> str: ...
    def getAvailableProcessors(self) -> int: ...
    def getName(self) -> str: ...
    def getSystemLoadAverage(self) -> float: ...
    def getVersion(self) -> str: ...

class PlatformLoggingMXBean(PlatformManagedObject):
    def getLoggerLevel(self, string: str) -> str: ...
    def getLoggerNames(self) -> java.util.List[str]: ...
    def getParentLoggerName(self, string: str) -> str: ...
    def setLoggerLevel(self, string: str, string2: str) -> None: ...

class RuntimeMXBean(PlatformManagedObject):
    def getBootClassPath(self) -> str: ...
    def getClassPath(self) -> str: ...
    def getInputArguments(self) -> java.util.List[str]: ...
    def getLibraryPath(self) -> str: ...
    def getManagementSpecVersion(self) -> str: ...
    def getName(self) -> str: ...
    def getPid(self) -> int: ...
    def getSpecName(self) -> str: ...
    def getSpecVendor(self) -> str: ...
    def getSpecVersion(self) -> str: ...
    def getStartTime(self) -> int: ...
    def getSystemProperties(self) -> java.util.Map[str, str]: ...
    def getUptime(self) -> int: ...
    def getVmName(self) -> str: ...
    def getVmVendor(self) -> str: ...
    def getVmVersion(self) -> str: ...
    def isBootClassPathSupported(self) -> bool: ...

class ThreadMXBean(PlatformManagedObject):
    @typing.overload
    def dumpAllThreads(self, boolean: bool, boolean2: bool) -> typing.MutableSequence[ThreadInfo]: ...
    @typing.overload
    def dumpAllThreads(self, boolean: bool, boolean2: bool, int: int) -> typing.MutableSequence[ThreadInfo]: ...
    def findDeadlockedThreads(self) -> typing.MutableSequence[int]: ...
    def findMonitorDeadlockedThreads(self) -> typing.MutableSequence[int]: ...
    def getAllThreadIds(self) -> typing.MutableSequence[int]: ...
    def getCurrentThreadCpuTime(self) -> int: ...
    def getCurrentThreadUserTime(self) -> int: ...
    def getDaemonThreadCount(self) -> int: ...
    def getPeakThreadCount(self) -> int: ...
    def getThreadCount(self) -> int: ...
    def getThreadCpuTime(self, long: int) -> int: ...
    @typing.overload
    def getThreadInfo(self, long: int) -> ThreadInfo: ...
    @typing.overload
    def getThreadInfo(self, long: int, int: int) -> ThreadInfo: ...
    @typing.overload
    def getThreadInfo(self, longArray: typing.Union[typing.List[int], jpype.JArray]) -> typing.MutableSequence[ThreadInfo]: ...
    @typing.overload
    def getThreadInfo(self, longArray: typing.Union[typing.List[int], jpype.JArray], boolean: bool, boolean2: bool) -> typing.MutableSequence[ThreadInfo]: ...
    @typing.overload
    def getThreadInfo(self, longArray: typing.Union[typing.List[int], jpype.JArray], int: int) -> typing.MutableSequence[ThreadInfo]: ...
    @typing.overload
    def getThreadInfo(self, longArray: typing.Union[typing.List[int], jpype.JArray], boolean: bool, boolean2: bool, int: int) -> typing.MutableSequence[ThreadInfo]: ...
    def getThreadUserTime(self, long: int) -> int: ...
    def getTotalStartedThreadCount(self) -> int: ...
    def isCurrentThreadCpuTimeSupported(self) -> bool: ...
    def isObjectMonitorUsageSupported(self) -> bool: ...
    def isSynchronizerUsageSupported(self) -> bool: ...
    def isThreadContentionMonitoringEnabled(self) -> bool: ...
    def isThreadContentionMonitoringSupported(self) -> bool: ...
    def isThreadCpuTimeEnabled(self) -> bool: ...
    def isThreadCpuTimeSupported(self) -> bool: ...
    def resetPeakThreadCount(self) -> None: ...
    def setThreadContentionMonitoringEnabled(self, boolean: bool) -> None: ...
    def setThreadCpuTimeEnabled(self, boolean: bool) -> None: ...

class GarbageCollectorMXBean(MemoryManagerMXBean):
    def getCollectionCount(self) -> int: ...
    def getCollectionTime(self) -> int: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("java.lang.management")``.

    BufferPoolMXBean: typing.Type[BufferPoolMXBean]
    ClassLoadingMXBean: typing.Type[ClassLoadingMXBean]
    CompilationMXBean: typing.Type[CompilationMXBean]
    GarbageCollectorMXBean: typing.Type[GarbageCollectorMXBean]
    LockInfo: typing.Type[LockInfo]
    ManagementFactory: typing.Type[ManagementFactory]
    ManagementPermission: typing.Type[ManagementPermission]
    MemoryMXBean: typing.Type[MemoryMXBean]
    MemoryManagerMXBean: typing.Type[MemoryManagerMXBean]
    MemoryNotificationInfo: typing.Type[MemoryNotificationInfo]
    MemoryPoolMXBean: typing.Type[MemoryPoolMXBean]
    MemoryType: typing.Type[MemoryType]
    MemoryUsage: typing.Type[MemoryUsage]
    MonitorInfo: typing.Type[MonitorInfo]
    OperatingSystemMXBean: typing.Type[OperatingSystemMXBean]
    PlatformLoggingMXBean: typing.Type[PlatformLoggingMXBean]
    PlatformManagedObject: typing.Type[PlatformManagedObject]
    RuntimeMXBean: typing.Type[RuntimeMXBean]
    ThreadInfo: typing.Type[ThreadInfo]
    ThreadMXBean: typing.Type[ThreadMXBean]
