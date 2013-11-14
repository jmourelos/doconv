.. _plugins:
============
Plugins
============

Introduction
============

Some of the plugins provide overlapping functionality, like asciidoc and
asciidoctor plugins. In that cases it suffices to install the dependencies for
one of the overlapping plugins.

Usually a plugin has some pre-requisites to be used. If doconv detects in the
system the dependencies needed for the plugin to work, the plugin will be enabled.

asciidoc
========

The asciidoc plugin converts from AsciiDoc to DocBook.

Pre-requisites for activation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

asciidoc_ should be installed:

.. _asciidoc: http://www.methods.co.nz/asciidoc/manpage.html

Arch Linux:: 

  $ pacman -S asciidoc

Debian/Ubuntu::

  $ apt-get install asciidoc

CentOS/Fedora:: 

  $ yum install asciidoc


See `asciidoc website <http://www.methods.co.nz/asciidoc/INSTALL.html#X2>`_ for
more information.

.. note:: asciidoc requires Python 2.x to be available in the system.

asciidoctor
===========


The asciidoctor plugin converts from AsciiDoc to DocBook. 

Pre-requisites for activation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

asciidoctor_ should be installed:

.. _asciidoctor: http://asciidoctor.org

See `asciidoctor website <http://asciidoctor.org/docs/install-toolchain>`_ for
installation instructions.

docbooktodita
=============


The docbooktodita plugin converts from DocBook to DITA. 

Pre-requisites for activation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are no pre-requisites.
