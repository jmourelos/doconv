Future
------

The long-term goal
++++++++++++++++++

The idea behind doconv is to develop a text format conversion tool based on a
plugin architecture. Each plugin will expose its conversion capabilities and
doconv will chain calls to the different plugins leveraging the capabilities
of each individual plugin.

To make clear the meaning of the previous paragraph: at this moment doconv has two
plugins (asciidoc plugin and docbooktodita plugin). If doconv is asked to convert
an AsciiDoc file to DITA, it will use the asciidoc plugin to convert the file
first to DocBook and then it will use the docbooktodita plugin to convert the
DocBook version to DITA.

If several plugins overlap in functionality it is not a problem, doconv will
choose which one to use.

A plugin can implement the conversion between two different formats or rely on
a third party tool for the conversion.

TODO
++++

- Add tests...
- Refactor a lot...
- New plugins that could add a lot of formats supported like pandoc or uniconv.
