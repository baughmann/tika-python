
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.awt.event
import java.io
import java.net
import javax.swing
import javax.swing.event
import jpype
import jpype.protocol
import org.apache.tika.parser
import typing



class TikaGUI(javax.swing.JFrame, java.awt.event.ActionListener, javax.swing.event.HyperlinkListener):
    def __init__(self, parser: org.apache.tika.parser.Parser): ...
    def actionPerformed(self, actionEvent: java.awt.event.ActionEvent) -> None: ...
    def hyperlinkUpdate(self, hyperlinkEvent: javax.swing.event.HyperlinkEvent) -> None: ...
    @staticmethod
    def main(stringArray: typing.Union[typing.List[str], jpype.JArray]) -> None: ...
    def openFile(self, file: typing.Union[java.io.File, jpype.protocol.SupportsPath]) -> None: ...
    def openURL(self, uRL: java.net.URL) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.gui")``.

    TikaGUI: typing.Type[TikaGUI]
