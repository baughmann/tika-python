
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import org.apache.tika.language.detect
import org.apache.tika.language.translate
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.language")``.

    detect: org.apache.tika.language.detect.__module_protocol__
    translate: org.apache.tika.language.translate.__module_protocol__
