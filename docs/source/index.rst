Welcome to tika-python's documentation!
=====================================

Overview
--------

.. include:: readme.rst

API Reference
============

.. toctree::
   :maxdepth: 2
   :caption: API Documentation

   tika

Testing
=======

.. toctree::
   :maxdepth: 2
   :caption: Test Documentation

   test

Developer Guide
=============

.. code-block:: python

   import tika
   from tika import parser
   
   # Parse a file
   parsed = parser.from_file('path/to/file')
   print(parsed["metadata"])
   print(parsed["content"])

   # Detect MIME type
   from tika import detector
   print(detector.from_file('path/to/file'))

   # Detect language
   from tika import language
   print(language.from_file('path/to/file'))

Indices and References
===================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`