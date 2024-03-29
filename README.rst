User under win32 should use `original mcomix`_.


================
Toggle View Mode
================

Fork from MComix3 with a small extra feature - a toggle between best fit and width fit.

I use vi-like motion keybinds (hjkl), and I map space to toggle view mode. I also set the steps required to flip a page to a high number, so I can scroll down a page in fit width mode, then hit space to zoom out into best fit and view the whole page I just read, flip a page, see it in full, then hit space to zoom back in. Perfect.

=======
MComix3
=======

Fork from MComix gtk3 branch, switch to python3.

Only tested under Linux.

Required:
---------
- **Python3** 3.8 or later. `1`_
- **PyGObject** 3.27 or later `2`_, with **GTK+ 3 gir bindings** 3.24 or later.
- **Pillow** 6.2.1 or later. `3`_ (`Latest version`_ is always recommended)

Recommended:
------------
- **unrar**, **rar** or **libunrar** to extract RAR archives. `4`_
- **7z** `5`_ (**p7zip** `6`_ for POSIX system) to extract 7Z and LHA archives.
- **p7zip** with rar codec (**p7zip-rar** on Debian-like systems, providing ``Codecs/Rar.so`` file) to extract RAR archives.
- **lha** `7`_ to extract LHA archives.
- **mupdf** `8`_ for PDF support.
- (FLIF is not supported anymore. `9`_)

Run:
----
``python3 mcomix/mcomixstarter.py <diretory, archive or image>``

Install:
--------
**setup.py is not working**

``python3 installer.py --srcdir=mcomix --target=<somewhere>``

then:

``python3 <somewere>/mcomix/mcomixstarter.py <directory, archive or image>``

.. _original mcomix: https://sourceforge.net/projects/mcomix/
.. _1: https://www.python.org/downloads/
.. _2: https://pygobject.readthedocs.io/
.. _3: https://pillow.readthedocs.io/
.. _Latest version: https://pypi.org/project/Pillow/
.. _4: https://www.rarlab.com/rar_add.htm
.. _5: https://www.7-zip.org/
.. _6: http://p7zip.sourceforge.net/
.. _7: https://fragglet.github.io/lhasa/
.. _8: https://mupdf.com/
.. _9: https://github.com/FLIF-hub/FLIF/commit/188d331a03f4c76cc4bc8a1b32f82dd569511be0
