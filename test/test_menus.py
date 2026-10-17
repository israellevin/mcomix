"""What the menu bar and the right-click menu hold, and the Help menu's
entries.

The menus are tuples in ui.py, so where an item stands is read from
them; what an item does is read from the window it was built for.
"""

import os
import unittest.mock

from gi.repository import GLib

from . import MComixTest, pump

from mcomix import constants
from mcomix import keybindings
from mcomix import icons
from mcomix import main
from mcomix import preferences_dialog
from mcomix import ui


def _submenu(layout, name):
    """The items of the submenu <name> in <layout>, at its top level."""
    return dict(item for item in layout if isinstance(item, tuple))[name]


def _names(layout):
    """Every action name in <layout> and its submenus."""
    for item in layout:
        if isinstance(item, tuple):
            yield item[0]
            yield from _names(item[1])
        elif item is not None:
            yield item


class LayoutTest(MComixTest):

    def test_the_menu_bar_ends_with_help(self):
        tops = [item[0] if isinstance(item, tuple) else item
                for item in ui._MENUBAR]
        self.assertEqual(['menu_file', 'menu_edit', 'menu_view', 'menu_go',
                          'menu_bookmarks', 'menu_image', 'menu_help'], tops)
        self.assertIn('about', _submenu(ui._MENUBAR, 'menu_help'))
        self.assertNotIn('about', _submenu(ui._MENUBAR, 'menu_file'))

    def test_the_right_click_menu_turns_the_page_too(self):
        """With the menu bar hidden it is the only menu there is, and it
        had no way to rotate or flip a page."""
        image = _submenu(ui._POPUP, 'menu_image_popup')
        self.assertEqual(_submenu(ui._MENUBAR, 'menu_image'), image)
        for name in ('rotate_90', 'rotate_270', 'flip_horiz',
                     'invert_color', 'enhance_image'):
            self.assertIn(name, set(_names(image)))

    def test_the_submenus_the_two_menus_share_are_the_same(self):
        for bar, popup in (('menu_view', 'menu_view_popup'),
                           ('menu_go', 'menu_go_popup')):
            self.assertEqual(_submenu(ui._MENUBAR, bar),
                             _submenu(ui._POPUP, popup))

    def test_the_shortcuts_tab_files_the_image_menu_s_keys_together(self):
        """Enhance and invert colours were filed under File, and the
        rotations under a group of their own."""
        top = [name for name in _submenu(ui._MENUBAR, 'menu_image')
               if isinstance(name, str)]
        groups = {keybindings.BINDING_INFO[name]['group'] for name in top
                  if name in keybindings.BINDING_INFO}
        self.assertEqual({'Image'}, groups)
        for name in ('preferences', 'edit_archive', 'undo'):
            self.assertEqual('Edit', keybindings.BINDING_INFO[name]['group'])

    def test_no_item_is_in_two_places_of_the_menu_bar(self):
        names = [name for name in _names(ui._MENUBAR)
                 if not name.startswith('menu_')]
        self.assertEqual(sorted(set(names)), sorted(names))


class HelpMenuTest(MComixTest):

    def setUp(self):
        super().setUp()
        for directory in (constants.CONFIG_DIR, constants.DATA_DIR,
                          constants.THUMBNAIL_PATH):
            os.makedirs(directory, exist_ok=True)
        icons.load_icons()
        self.window = main.MainWindow()
        main.set_main_window(self.window)
        pump()

    def tearDown(self):
        preferences_dialog._close_dialog()
        self.window.terminate_program()
        self.window.destroy()
        main.set_main_window(None)
        pump()
        super().tearDown()

    def test_the_manual_is_handed_to_the_desktop_s_browser(self):
        with unittest.mock.patch.object(ui.Gtk, 'UriLauncher') as launcher:
            self.window.actiongroup.get_action('manual').activate()
        launcher.new.assert_called_once_with(constants.MANUAL_URL)
        launch = launcher.new.return_value.launch
        self.assertEqual(1, launch.call_count)
        self.assertIs(self.window, launch.call_args.args[0])

    def test_a_manual_that_cannot_be_opened_says_why(self):
        launcher = unittest.mock.Mock()
        launcher.launch_finish.side_effect = GLib.Error('no browser')
        with unittest.mock.patch.object(self.window.osd, 'show') as show:
            self.window.uimanager._manual_shown(launcher, None)
        show.assert_called_once_with(
            'Could not open the manual: no browser')

    def test_keyboard_shortcuts_opens_the_preferences_on_their_tab(self):
        self.window.actiongroup.get_action('shortcuts').activate()
        pump()
        dialog = preferences_dialog._dialog
        self.assertIsNotNone(dialog)
        self.assertIs(dialog.shortcuts, dialog.notebook.get_nth_page(
            dialog.notebook.get_current_page()))

    def test_it_turns_an_open_dialog_to_that_tab_as_well(self):
        self.window.actiongroup.get_action('preferences').activate()
        pump()
        dialog = preferences_dialog._dialog
        dialog.notebook.set_current_page(0)
        self.window.actiongroup.get_action('shortcuts').activate()
        pump()
        self.assertIs(dialog, preferences_dialog._dialog)
        self.assertIs(dialog.shortcuts, dialog.notebook.get_nth_page(
            dialog.notebook.get_current_page()))


# vim: expandtab:sw=4:ts=4
