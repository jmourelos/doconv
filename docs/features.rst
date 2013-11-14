Features
--------

* Conversion from AsciiDoc to DITA
* Conversion from DocBook to DITA
* Plugins' orchestration to perform conversions not achievable by a single
  plugin
* Easily extensible to add new plugins

Available Format Conversions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. graphviz:: ../conversions.dot

Each node of the graph represents a document format. Each arrow represents the
conversion between two formats (being provided by the plugin labeling the
arrow). Note that some arrows are unidirectional indicating that the conversion
only works in one way.
