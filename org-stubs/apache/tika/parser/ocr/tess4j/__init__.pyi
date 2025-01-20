
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.awt.image
import typing



class ImageDeskew:
    def __init__(self, bufferedImage: java.awt.image.BufferedImage): ...
    def getAlpha(self, int: int) -> float: ...
    def getSkewAngle(self) -> float: ...
    class HoughLine:
        count: int = ...
        index: int = ...
        alpha: float = ...
        d: float = ...
        def __init__(self): ...

class ImageUtil:
    def __init__(self): ...
    @typing.overload
    @staticmethod
    def isBlack(bufferedImage: java.awt.image.BufferedImage, int: int, int2: int) -> bool: ...
    @typing.overload
    @staticmethod
    def isBlack(bufferedImage: java.awt.image.BufferedImage, int: int, int2: int, int3: int) -> bool: ...
    @staticmethod
    def rotate(bufferedImage: java.awt.image.BufferedImage, double: float, int: int, int2: int) -> java.awt.image.BufferedImage: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.parser.ocr.tess4j")``.

    ImageDeskew: typing.Type[ImageDeskew]
    ImageUtil: typing.Type[ImageUtil]
