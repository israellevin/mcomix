""" MComix' own icons, as an icon theme finds them. """

import glob
import os
import re
from xml.etree import ElementTree

from gi.repository import Gtk
from PIL import Image

from . import MComixTest

from mcomix import icons

#: The checkout: the desktop's copies of the icon are under share/.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class OwnIconsTest(MComixTest):

    def test_loading_them_again_adds_nothing_to_the_search(self):
        """Every test that builds a window loads the icons, and each load
        put MComix' directory on the display's search path once more:
        after two hundred tests an icon lookup went through two hundred
        copies of it, and presenting a window took 70 ms instead of 1."""
        icons.load_icons()
        icons.load_icons()
        path = icons.icon_theme().get_search_path()
        self.assertEqual(1, path.count(icons.icon_search_path()))

    def _theme(self):
        """An icon theme that searches MComix' own icons and nothing
        else: whatever it finds, the program carries."""
        theme = Gtk.IconTheme()
        theme.set_search_path([icons.icon_search_path()])
        return theme

    def test_the_window_icon_is_among_them(self):
        """main.py names the window icon "mcomix", which only a copy
        installed under share/icons supplied: pip installs none, and the
        Windows build collects MSYS2's hicolor theme, which has no MComix
        in it, so the window went without its icon."""
        theme = self._theme()
        self.assertTrue(theme.has_icon('mcomix'))
        for size in (16, 48, 256):
            with self.subTest(size=size):
                found = theme.lookup_icon('mcomix', None, size, 1,
                                          Gtk.TextDirection.NONE, 0)
                self.assertTrue(found.get_file().get_path().endswith(
                    'mcomix.png'))

    def test_the_toolbar_icons_are_among_them(self):
        """So that the test above, which finds nothing in a theme that
        cannot read the directory, says something."""
        self.assertTrue(self._theme().has_icon('mcomix-archive'))


class IconSizesTest(MComixTest):

    def test_each_picture_is_the_size_its_folder_names(self):
        """An icon theme's <N>x<N> folder holds pictures N pixels square.
        The application icon is 4:3 and was exported N pixels wide only:
        16x12 in 16x16, 256x192 in 256x256, which Debian's lintian
        reports (upstream bug 159) and a theme may stretch."""
        found = glob.glob(os.path.join(ROOT, '**', 'hicolor', '*x*', '**',
                                       '*.png'), recursive=True)
        self.assertGreater(len(found), 12)
        wrong = []
        for path in found:
            folder = re.search(r'[/\\](\d+)x(\d+)[/\\]', path)
            with Image.open(path) as image:
                if image.size != (int(folder[1]), int(folder[2])):
                    wrong.append((os.path.relpath(path, ROOT), image.size))
        self.assertEqual([], wrong)

    def test_each_scalable_picture_is_square(self):
        """flatpak build-export refuses an application icon that is not
        square ("Expected a square icon but got: 3540x2655"), which
        stopped the Flatpak of 26.10; the 4:3 picture sits centred on a
        square page."""
        found = glob.glob(os.path.join(ROOT, '**', 'hicolor', 'scalable',
                                       '**', '*.svg'), recursive=True)
        self.assertGreater(len(found), 1)
        wrong = []
        for path in found:
            root = ElementTree.parse(path).getroot()
            view_box = [float(n) for n in root.get('viewBox').split()]
            if (root.get('width') != root.get('height')
                    or view_box[2] != view_box[3]):
                wrong.append(os.path.relpath(path, ROOT))
        self.assertEqual([], wrong)
