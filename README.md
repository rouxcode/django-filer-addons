# django-filer-addons


[![CI](https://github.com/rouxcode/django-filer-aaddons/actions/workflows/ci.yml/badge.svg)](https://github.com/rouxcode/django-filer-addons/actions/workflows/ci.yml)

[//]: # ([![PyPi Version]&#40;https://img.shields.io/pypi/v/django-filer-addons.svg "PyPi Version"&#41;]&#40;https://pypi.python.org/pypi/django-filer-addons/&#41;)

[//]: # ([![Licence]&#40;https://img.shields.io/pypi/l/django-filer-addons.svg "Licence"&#41;]&#40;https://pypi.python.org/pypi/django-filer-addons/&#41;)

various django-filer enhancements / bugfixes. Fair warning: parts of this package might not be
best practiced or very efficient (that said, can cause performance issues!), but are implemented
as we needed this functionality, and as filer development sometimes
seems to stall, it is was implemented just to make it work. Part of this package might even get merged
into filer (someday..).

Features
--------

This package provides sub applications, that can be installed individually, to only selecte the
needed features.

- `filer_addons.filer_gui` - an improved filer file and filer image field, a multiupload inline.
- `filer_addons.filer_signals` - can help avoid duplicates, will rename files on the filesystem if
  said to do so, and can put unfiled files in a default folder, to prevent permission issues.
- `filer_addons.filer_utils` - various helpers: for now, generate folder/filenames for uploaded
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
