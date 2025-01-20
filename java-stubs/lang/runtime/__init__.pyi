
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang.invoke
import typing



class ObjectMethods:
    @staticmethod
    def bootstrap(lookup: java.lang.invoke.MethodHandles.Lookup, string: str, typeDescriptor: typing.Union[java.lang.invoke.TypeDescriptor, typing.Callable], class_: typing.Type[typing.Any], string2: str, *methodHandle: java.lang.invoke.MethodHandle) -> typing.Any: ...

class SwitchBootstraps:
    @staticmethod
    def enumSwitch(lookup: java.lang.invoke.MethodHandles.Lookup, string: str, methodType: java.lang.invoke.MethodType, *object: typing.Any) -> java.lang.invoke.CallSite: ...
    @staticmethod
    def typeSwitch(lookup: java.lang.invoke.MethodHandles.Lookup, string: str, methodType: java.lang.invoke.MethodType, *object: typing.Any) -> java.lang.invoke.CallSite: ...

class TemplateRuntime:
    @staticmethod
    def newLargeStringTemplate(lookup: java.lang.invoke.MethodHandles.Lookup, string: str, methodType: java.lang.invoke.MethodType) -> java.lang.invoke.CallSite: ...
    @staticmethod
    def newStringTemplate(lookup: java.lang.invoke.MethodHandles.Lookup, string: str, methodType: java.lang.invoke.MethodType, *string2: str) -> java.lang.invoke.CallSite: ...
    @staticmethod
    def processStringTemplate(lookup: java.lang.invoke.MethodHandles.Lookup, string: str, methodType: java.lang.invoke.MethodType, methodHandle: java.lang.invoke.MethodHandle, *string2: str) -> java.lang.invoke.CallSite: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("java.lang.runtime")``.

    ObjectMethods: typing.Type[ObjectMethods]
    SwitchBootstraps: typing.Type[SwitchBootstraps]
    TemplateRuntime: typing.Type[TemplateRuntime]
