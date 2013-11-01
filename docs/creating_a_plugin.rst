Creating a plugin
-----------------

Creating a plugin should be quite easy, it requires 3 steps:

* Extend the base plugin class, implementing these abstract methods:

  .. autoclass:: doconv.plugin.base.PluginBase
     :members:


* If the plugin requires some external files, for example XSLT files, store them in a directory with the plugin's name and remember to add the directory to the MANIFEST.in.

* Add an entry point for your new plugin to *setup.py*::

    entry_points={
        'console_scripts': [
            'doconv = doconv.doconv:main'
            ],
        'doconv.converter': [
            'asciidoc = doconv.plugin.asciidoc:AsciiDoc',
            'docbooktodita = doconv.plugin.docbooktodita:DocBookToDita',
            'yournewplugin = doconv.plugin.yournewplugin:YourNewPlugin',
            ],
        },


You are done! In case you would like to contribute your new plugin, see :ref:`how to contribute <contributing>`.
