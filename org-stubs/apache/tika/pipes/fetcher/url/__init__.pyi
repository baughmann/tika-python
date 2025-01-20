
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import org.apache.tika.metadata
import org.apache.tika.parser
import org.apache.tika.pipes.fetcher
import typing



class UrlFetcher(org.apache.tika.pipes.fetcher.AbstractFetcher):
    def __init__(self): ...
    def fetch(self, string: str, metadata: org.apache.tika.metadata.Metadata, parseContext: org.apache.tika.parser.ParseContext) -> java.io.InputStream: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.apache.tika.pipes.fetcher.url")``.

    UrlFetcher: typing.Type[UrlFetcher]
