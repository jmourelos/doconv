============
Installation
============


Pre-requisites
==============

In addition to any dependency described in the installation section some plugins require
additional dependencies to be enabled. See the :ref:`plugins section <plugins>` for more information.

Arch Linux
==========

doconv is available in AUR, it can be installed using a tool like yaourt::

    $ sudo yaourt -S doconv

Other distributions (generic installation)
==========================================

Some development dependencies need to be installed. In Ubuntu would be::

    $ sudo apt-get install libxml2-dev libxslt1-dev python-dev

Then install latest stable doconv version using pip_::

    $ pip install doconv

or, if administrative privileges are needed::

    $ sudo pip install doconv

.. _pip: http://pypi.python.org/pypi/pip
