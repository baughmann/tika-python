
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java
import java.awt
import java.io
import java.lang
import javax.print_
import javax.print_.attribute
import typing



class Book(java.awt.print_.Pageable):
    def __init__(self): ...
    @typing.overload
    def append(self, printable: typing.Union['Printable', typing.Callable], pageFormat: 'PageFormat') -> None: ...
    @typing.overload
    def append(self, printable: typing.Union['Printable', typing.Callable], pageFormat: 'PageFormat', int: int) -> None: ...
    def getNumberOfPages(self) -> int: ...
    def getPageFormat(self, int: int) -> 'PageFormat': ...
    def getPrintable(self, int: int) -> 'Printable': ...
    def setPage(self, int: int, printable: typing.Union['Printable', typing.Callable], pageFormat: 'PageFormat') -> None: ...

class PageFormat(java.lang.Cloneable):
    LANDSCAPE: typing.ClassVar[int] = ...
    PORTRAIT: typing.ClassVar[int] = ...
    REVERSE_LANDSCAPE: typing.ClassVar[int] = ...
    def __init__(self): ...
    def clone(self) -> typing.Any: ...
    def getHeight(self) -> float: ...
    def getImageableHeight(self) -> float: ...
    def getImageableWidth(self) -> float: ...
    def getImageableX(self) -> float: ...
    def getImageableY(self) -> float: ...
    def getMatrix(self) -> typing.MutableSequence[float]: ...
    def getOrientation(self) -> int: ...
    def getPaper(self) -> 'Paper': ...
    def getWidth(self) -> float: ...
    def setOrientation(self, int: int) -> None: ...
    def setPaper(self, paper: 'Paper') -> None: ...

class Pageable:
    UNKNOWN_NUMBER_OF_PAGES: typing.ClassVar[int] = ...
    def getNumberOfPages(self) -> int: ...
    def getPageFormat(self, int: int) -> PageFormat: ...
    def getPrintable(self, int: int) -> 'Printable': ...

class Paper(java.lang.Cloneable):
    def __init__(self): ...
    def clone(self) -> typing.Any: ...
    def getHeight(self) -> float: ...
    def getImageableHeight(self) -> float: ...
    def getImageableWidth(self) -> float: ...
    def getImageableX(self) -> float: ...
    def getImageableY(self) -> float: ...
    def getWidth(self) -> float: ...
    def setImageableArea(self, double: float, double2: float, double3: float, double4: float) -> None: ...
    def setSize(self, double: float, double2: float) -> None: ...

class Printable:
    PAGE_EXISTS: typing.ClassVar[int] = ...
    NO_SUCH_PAGE: typing.ClassVar[int] = ...
    def print_(self, graphics: java.awt.Graphics, pageFormat: PageFormat, int: int) -> int: ...

class PrinterAbortException(java.awt.print_.PrinterException):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: str): ...

class PrinterException(java.lang.Exception):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: str): ...

class PrinterGraphics:
    def getPrinterJob(self) -> 'PrinterJob': ...

class PrinterIOException(PrinterException):
    def __init__(self, iOException: java.io.IOException): ...
    def getCause(self) -> java.lang.Throwable: ...
    def getIOException(self) -> java.io.IOException: ...

class PrinterJob:
    def __init__(self): ...
    def cancel(self) -> None: ...
    @typing.overload
    def defaultPage(self, pageFormat: PageFormat) -> PageFormat: ...
    @typing.overload
    def defaultPage(self) -> PageFormat: ...
    def getCopies(self) -> int: ...
    def getJobName(self) -> str: ...
    def getPageFormat(self, printRequestAttributeSet: javax.print_.attribute.PrintRequestAttributeSet) -> PageFormat: ...
    def getPrintService(self) -> javax.print_.PrintService: ...
    @staticmethod
    def getPrinterJob() -> 'PrinterJob': ...
    def getUserName(self) -> str: ...
    def isCancelled(self) -> bool: ...
    @staticmethod
    def lookupPrintServices() -> typing.MutableSequence[javax.print_.PrintService]: ...
    @staticmethod
    def lookupStreamPrintServices(string: str) -> typing.MutableSequence[javax.print_.StreamPrintServiceFactory]: ...
    @typing.overload
    def pageDialog(self, pageFormat: PageFormat) -> PageFormat: ...
    @typing.overload
    def pageDialog(self, printRequestAttributeSet: javax.print_.attribute.PrintRequestAttributeSet) -> PageFormat: ...
    @typing.overload
    def printDialog(self) -> bool: ...
    @typing.overload
    def printDialog(self, printRequestAttributeSet: javax.print_.attribute.PrintRequestAttributeSet) -> bool: ...
    @typing.overload
    def print_(self) -> None: ...
    @typing.overload
    def print_(self, printRequestAttributeSet: javax.print_.attribute.PrintRequestAttributeSet) -> None: ...
    def setCopies(self, int: int) -> None: ...
    def setJobName(self, string: str) -> None: ...
    def setPageable(self, pageable: Pageable) -> None: ...
    def setPrintService(self, printService: javax.print_.PrintService) -> None: ...
    @typing.overload
    def setPrintable(self, printable: typing.Union[Printable, typing.Callable]) -> None: ...
    @typing.overload
    def setPrintable(self, printable: typing.Union[Printable, typing.Callable], pageFormat: PageFormat) -> None: ...
    def validatePage(self, pageFormat: PageFormat) -> PageFormat: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("java.awt.print_")``.

    Book: typing.Type[Book]
    PageFormat: typing.Type[PageFormat]
    Pageable: typing.Type[Pageable]
    Paper: typing.Type[Paper]
    Printable: typing.Type[Printable]
    PrinterAbortException: typing.Type[PrinterAbortException]
    PrinterException: typing.Type[PrinterException]
    PrinterGraphics: typing.Type[PrinterGraphics]
    PrinterIOException: typing.Type[PrinterIOException]
    PrinterJob: typing.Type[PrinterJob]
