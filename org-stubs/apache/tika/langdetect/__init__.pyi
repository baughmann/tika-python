
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import org.apache.tika.langdetect.optimaize
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.langdetect")``.

    optimaize: org.apache.tika.langdetect.optimaize.__module_protocol__
