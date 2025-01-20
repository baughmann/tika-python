#!/usr/bin/env python
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from typing import BinaryIO

from tika.core import get_config


def get_parsers() -> str | bytes | BinaryIO:
    """Retrieves the list of available parsers from the Tika server.

    Fetches detailed information about all parsers supported by the Tika server,
    including their supported MIME types and parser properties.

    Returns:
        A response containing the parser configuration, typically as JSON. The return
        type matches the server response format, which may be str, bytes, or BinaryIO.

    Raises:
        TikaError: If the server request fails or returns an error status.

    Example:
        >>> parsers = get_parsers()
        >>> print(parsers)  # Prints JSON of available parsers and their capabilities
    """
    return get_config("parsers")[1]


def get_mime_types() -> str | bytes | BinaryIO:
    """Retrieves the list of supported MIME types from the Tika server.

    Fetches the complete list of MIME types that the Tika server can handle,
    including file extensions and type hierarchies.

    Returns:
        A response containing the MIME type configuration, typically as JSON. The return
        type matches the server response format, which may be str, bytes, or BinaryIO.

    Raises:
        TikaError: If the server request fails or returns an error status.

    Example:
        >>> mime_types = get_mime_types()
        >>> print(mime_types)  # Prints JSON of supported MIME types
    """
    return get_config("mime-types")[1]


def get_detectors() -> str | bytes | BinaryIO:
    """Retrieves the list of available content detectors from the Tika server.

    Fetches information about all content type detectors supported by the Tika server,
    including their detection capabilities and priorities.

    Returns:
        A response containing the detector configuration, typically as JSON. The return
        type matches the server response format, which may be str, bytes, or BinaryIO.

    Raises:
        TikaError: If the server request fails or returns an error status.

    Example:
        >>> detectors = get_detectors()
        >>> print(detectors)  # Prints JSON of available detectors
    """
    return get_config("detectors")[1]
