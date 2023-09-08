Documentation
===

[TOC]

Please note that this site is an ongoing effort to create a somewhat usable user manual for MComix.

Installation
---

Instructions for installing MComix can be found on the [Installation] page.


The main window
---

In the default configuration, MComix' user interface will look somewhat similar to the following screenshot. The main areas of interest are the tool- and menubar, the thumbnail sidebar on the left, and the display port in the center.

[[img src="mcomix-mainwindow.png" alt="MComix' main window"]]

This configuration is normally acceptable for general image viewing purposes. For reading comics, you will likely want a more uncluttered interface. This can be archived either by pressing the "F" key to enter fullscreen mode, or by hiding various UI elements by disabling them with "View &rarr; Toolbars". The "I" key also hides all user interface elements. Normally, you will also want to switch from "Best fit" mode to "Fit to width" mode by pressing the "W" key. This way, images will only be scaled down to fit the screen width, not both width and height.

Paging and scrolling from one image to the next works similarly to most other image viewers. The arrow keys scroll the page, while PageDown and PageUp will switch to the next and previous pages.

### Fit modes ###

MComix has several automatic fit modes that scale down images by certain criteria. Those are:

- Best fit - Images are scaled down to fit within the window.
- Fit to width - Images are scaled down to fit the screen width. If an image is higher than the screen, it can be scrolled up and down.
- Fit to height - Images are scaled down to fit the screen height. If an image is wider than the screen,
it can be scrolled left and right.
- Fit to size - Resize images to either a certain height or a certain width. Size in pixel and width or height can be set up in the preferences dialog. In the default configuration, this mode resizes an image to 1200px in height.
- Manual zoom mode - No scaling is performed on the image.

Normally, no mode will increase an image's size by scaling it up. If such behavior is desired, "View &rarr; Stretch small images" enables scaling in both directions, up and down.

### Double page mode and manga mode ###

Normally, MComix will only show one image at a time. For reading comics, especially on widescreen monitors, it can be desirable to display two images at once next to each other. This way, reading comics becomes more natural and double-page spreads can be viewed without having to edit the image files. Double-page mode is toggled by pressing "D". Unless set up otherwise, the first page of an archive or directory will always be displayed alone (representing the book cover). Pages with width exceeding height will also be displayed alone.

When changing pages in double-page mode, MComix will automatically forward or backward two pages at once. To forward only one page, hold the CTRL key while switching pages.

By default, MComix will arrange pages left-to-right, and also scroll in this direction. For manga, MComix has a special "Manga mode" activated by pressing "M". This mode lays out pages right-to-left, and changes scrolling accordingly.

### Slideshow mode ###

MComix can automatically scroll and switch pages by activating slideshow mode, using CTRL+S. Conceptually, this works the same way as pressing the "Down" arrow key repeatedly with a certain interval between each keypress. The delay and amount of pixels scrolled can be customized in the preferences dialog.

By default, MComix will scroll down 50 pixels every three seconds. For a smoother experience, the following settings might be worth a try:

- Slideshow delay: 0.05 seconds
- Slideshow step: 1 px

### Keybindings ###

For all key bindings available, please refer to [Keybindings].

Preferences
---

To customize MComix, you can press the "F12" key to open the preferences dialog. All options are documented on the [Preferences] page.

The book library
---

MComix also has a library for organizing and keeping track of comic books. While it in no way is meant to replace a full-featured file manager, being able to categorize books into collections and showing a list of all book covers should normally be enough to allow the user quick access to his favorite books. The library only adds archives, not directories. So, a "book" in this context refers to a single archive of any format MComix can open.

[[img src="mcomix-library.png" alt="Library window"]]

The left side shows a list of collections, while the right side shows all books within the selected collection. The collection "All books" is special, as it automatically contains all books in every single collection. Collections can be nested by dragging and dropping one collection into any other collection. When a collection is selected, books will be shown from the collection itself and from any children collections.

A new collection can be added by right-clicking into the collection list and choosing "New". Books can be added by right-clicking on any collection and clicking "Add". The following dialog allows the user to either create a new collection for the selected books, or to place them in the currently selected collection.

Right-clicking into the book view allows for adding and removing books, opening of the selected books, and customizing the library view by choosing thumbnail size and sort order.

### Library watch list ###

By using the watch list, MComix can keep track of certain directories and automatically add new books to the library when they are added to those directories. Every time the library is opened, new directories will be scanned, and books that aren't part of the library yet will be added.

### Recent books ###

When "Store information about recently opened files" is enabled in MComix' preferences window, all archives that are opened from within the program will automatically be added to a collection called "Recent". From here, they can be moved to other collections if desired.

Execute external programs
---

MComix can run a list of user-defined commands on the currently opened file/directory/archive. This might include external image viewers, file management tools or custom shell scripts. Please see [External_Commands] for more information.
