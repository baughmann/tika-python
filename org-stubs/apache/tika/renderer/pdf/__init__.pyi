
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import org.apache.tika.renderer.pdf.mutool
import org.apache.tika.renderer.pdf.pdfbox
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.renderer.pdf")``.

    mutool: org.apache.tika.renderer.pdf.mutool.__module_protocol__
    pdfbox: org.apache.tika.renderer.pdf.pdfbox.__module_protocol__
