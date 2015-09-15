import os
import sys
import urwid
import click
from glob import glob
from collections import defaultdict
from xdg.DesktopEntry import DesktopEntry
from cursedxdg.tui import CascadingBoxes, menu, sub_menu, menu_button,\
    exit_program


class CursedXDG(object):
    """
        CursedXDG
    """

    def __init__(self, appdir="/usr/share/applications/", palette=False):
        self.appdir = appdir
        self.apps = glob(os.path.join(self.appdir, '*.desktop'))
        self.palette = palette
        self.windows = [False]
        if not self.palette:
            self.palette = [
                ('banner', 'black', 'light gray'),
                ('streak', 'black', 'dark red'),
                ('bg', 'black', 'dark blue'), ]

    @property
    def categorized_menus(self):
        """
            Read the menus and return them in an array
        """
        result = defaultdict(list)
        for entry in [DesktopEntry(entry) for entry in self.apps]:
            try:
                category = entry.getCategories().pop()
                result[category].append(entry)
            except IndexError:
                pass
        return result

    @property
    def menu_tree(self):
        exit_btn = [menu_button('Exit', False, exit_program)]

        for menu_category, items in self.categorized_menus.items():
            cat = []
            for item in items:
                cat.append(menu_button(item.getName(), item.getExec(),
                                       lambda _, x: sys.exit(os.system(x))))
            yield sub_menu(menu_category, cat, self.windows)

        yield exit_btn

    def main(self):
        self.windows[0] = CascadingBoxes(menu('Main menu', self.menu_tree))
        urwid.MainLoop(self.windows[0], self.palette).run()


@click.command()
@click.option('--appdir', default="/usr/share/applications/",
              help="Where to find .desktop files")
def main(appdir=False):
    return CursedXDG(appdir).main()


if __name__ == "__main__":
    main()
