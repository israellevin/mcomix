"""Portability functions for MComix."""

import sys
import locale
import ctypes


def uri_prefix() -> str:
    """ The prefix used for creating file URIs. This is 'file://' on
    Linux, but 'file:' on Windows due to urllib using a different
    URI creating scheme here. """
    if sys.platform == 'win32':
        return 'file:'
    else:
        return 'file://'


def normalize_uri(uri: str) -> str:
    """ Normalize URIs passed into the program by different applications,
    normally via drag-and-drop. """

    if uri.startswith('file://localhost/'):  # Correctly formatted.
        return uri[16:]
    elif uri.startswith('file:///'):  # Nautilus etc.
        return uri[7:]
    elif uri.startswith('file:/'):  # Xffm etc.
        return uri[5:]
    else:
        return uri


def invalid_filesystem_chars() -> str:
    """ List of characters that cannot be used in filenames on the target platform. """
    if sys.platform == 'win32':
        return r':*?"<>|' + "".join([chr(i) for i in range(0, 32)])
    else:
        return ''


def get_default_locale() -> str:
    """ Gets the user's default locale. """
    if sys.platform == 'win32':
        windll = ctypes.windll.kernel32
        code = windll.GetUserDefaultUILanguage()
        return locale.windows_locale[code]
    else:
        lang, _ = locale.getdefaultlocale(('LANGUAGE', 'LC_ALL', 'LC_MESSAGES', 'LANG'))
        if lang:
            return str(lang)
        else:
            return "C"

# vim: expandtab:sw=4:ts=4
