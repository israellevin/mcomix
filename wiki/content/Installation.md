Installation instructions
===

No installation - Extract and go
---

For trying out MComix, no installation is necessary at all. Simply extract the MComix sources into a directory of your choosing and run mcomixstarter.py. Administrative privileges are not required.

    :::bash
    ~ $ unzip mcomix-versionno.zip
    ~ $ python mcomix-versionno/mcomixstarter.py

Note for Windows users: This method comes with a drawback on Windows – no executable wrapper is provided in the source distribution of MComix. Windows cannot easily associate Python script files with file types, for example, in the “Open with” context menu. It is therefore recommended to download the "All-in-one" version of MComix, which already includes a simple executable wrapper.

To uninstall MComix, simply delete the extracted MComix directory and MComix' settings directory. It can be found in your user directory, usually `~/.config/mcomix` on Linux and `%HOMEPATH%/MComix` on Windows.


Installation on Linux
---

By now, MComix is available in most major distributions' packaging systems, and should be installed using the distribution's system mechanism if possible. For others, manual installation is still available.

Run `python setup.py` install as root. This will install MComix in the `site-packages` folder of your Python installation. An executable `mcomix` will be placed in `/usr/bin`.

In order to install MComix in another base directory, use the `--prefix` option. The option `--user` explicitly installs MComix in the user's home directory, which does not need root access.

    :::bash
    ~ # unzip mcomix-0.99.zip
    ~ # python mcomix-0.99/setup.py --prefix /usr install

Installation on Windows
---

The all-in-one version includes all dependencies and a pre-built executable. After extraction, simply run `MComix.exe`.

To uninstall MComix, delete the directory MComix was extracted to, and MComix' settings directory, which can be found unter `%HOMEPATH%/MComix`.
