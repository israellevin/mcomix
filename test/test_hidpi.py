"""Pages on a screen with more pixels than the window has.

At a scale of 200 per cent there are two of the screen's pixels to each
of the window's along a side.  The pages are laid out in the window's
pixels, as everything else is, and were scaled to that layout alone, so
GTK drew them twice as large as they had been scaled: blurred.  They
are now scaled to the screen's pixels and drawn into the layout's box.
"""

import os
import unittest.mock

from gi.repository import Gdk

from . import MComixTest, get_testfile_path, pump, wait_for

from mcomix import constants
from mcomix import icons
from mcomix import keybindings
from mcomix import main


class DeviceScaleTest(MComixTest):

    def setUp(self):
        super().setUp()
        for directory in (constants.CONFIG_DIR, constants.DATA_DIR,
                          constants.THUMBNAIL_PATH):
            os.makedirs(directory, exist_ok=True)
        icons.load_icons()
        keybindings._manager = None
        self.window = main.MainWindow()
        main.set_main_window(self.window)

    def tearDown(self):
        self.window.terminate_program()
        self.window.destroy()
        main.set_main_window(None)
        pump()
        super().tearDown()

    def _draw_at(self, scale):
        with unittest.mock.patch.object(main.MainWindow, 'device_scale',
                                        return_value=scale):
            self.window.filehandler.open_file(
                get_testfile_path('images', 'landscape-no-exif.jpg'))
            self.assertTrue(wait_for(
                lambda: self.window.imagehandler.get_number_of_pages() > 0))
            pump()
            self.window.draw_image()
            pump()
        box = self.window.layout.get_content_boxes()[0].get_size()
        return box, self.window.images[0].get_paintable()

    def test_at_twice_the_pixels_the_page_is_scaled_to_them(self):
        (width, height), shown = self._draw_at(2.0)
        # Laid out where it was, at the window's size...
        self.assertEqual((width, height), (shown.get_intrinsic_width(),
                                           shown.get_intrinsic_height()))
        # ...from a picture with the screen's pixels in it.
        texture = shown._texture
        self.assertEqual((2 * width, 2 * height),
                         (texture.get_width(), texture.get_height()))

    def test_a_fractional_scale_rounds_to_whole_pixels(self):
        (width, height), shown = self._draw_at(1.5)
        texture = shown._texture
        self.assertEqual((round(1.5 * width), round(1.5 * height)),
                         (texture.get_width(), texture.get_height()))

    def test_at_one_pixel_to_one_the_page_is_a_plain_texture(self):
        (width, height), shown = self._draw_at(1.0)
        self.assertIsInstance(shown, Gdk.Texture)
        self.assertEqual((width, height),
                         (shown.get_width(), shown.get_height()))

    def test_the_scale_is_asked_of_the_window_s_surface(self):
        pump()
        surface = self.window.get_surface()
        self.assertIsNotNone(surface)
        with unittest.mock.patch.object(type(surface), 'get_scale',
                                        return_value=1.25):
            self.assertEqual(1.25, self.window.device_scale())

    def test_a_window_without_a_surface_counts_one_to_one(self):
        with unittest.mock.patch.object(main.MainWindow, 'get_surface',
                                        return_value=None):
            self.assertEqual(1.0, self.window.device_scale())


# vim: expandtab:sw=4:ts=4
