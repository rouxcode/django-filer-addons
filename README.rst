django-filer-addons
===================

.. image:: https://travis-ci.org/rouxcode/django-filer-addons.svg
    :target: https://travis-ci.org/rouxcode/django-filer-addons/
.. image:: https://img.shields.io/pypi/v/django-filer-addons.svg
    :target: https://pypi.python.org/pypi/django-filer-addons/
.. image:: https://img.shields.io/pypi/l/django-filer-addons.svg
    :target: https://pypi.python.org/pypi/django-filer-addons/

Various django-filer enhancements.

Features
--------

This package provides sub applications, that can be installed individually, to only selecte the
needed features.

- `filer_addons.filer_gui` - an improved filer file and filer image field, a multiupload inline.
- `filer_addons.filer_signals` - can help avoid duplicates, will rename files on the filesystem if \
said to do so, and can put unfiled files in a default folder, to prevent permission issues.
- `filer_addons.filer_utils` - various helpers: for now, generate folder/filenames for uploaded \
files (without folder/8-char simple uuid4/use db folder/year/year-month)

Install
-------

TODO

Usage
-----

TODO

**filer_gui**

**filer_signals**

**filer_utils**
