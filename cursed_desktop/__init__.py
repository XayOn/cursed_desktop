import os
import urwid
import click
import tmuxp
from collections import defaultdict
from xdg.DesktopEntry import DesktopEntry
from cursed_desktop.tui import (CascadingBoxes, menu,
                                sub_menu, menu_button,
                                exit_program)


class CursedXDG(object):
    """
        CursedXDG
    """

    def __init__(self, appdir="/usr/share/applications/", palette=False,
                 executor="tmux", filter_terminal=True):
        self.appdir = appdir
        self.filter_terminal = filter_terminal
        self.apps = []
        for path, _, files in os.walk(appdir):
            self.apps.extend([os.path.join(path, f)
                              for f in files if f.endswith('desktop')])
        self.palette = palette
        self.windows = [False]
        if not self.palette:
            self.palette = [
                ('banner', 'black', 'light gray'),
                ('streak', 'black', 'dark red'),
                ('bg', 'black', 'dark blue'), ]
        self.execute = getattr(self, executor)

    @property
    def categorized_menus(self):
        """
            Read the menus and return them in an array
        """
        result = defaultdict(list)
        for entry in [DesktopEntry(entry) for entry in self.apps]:
            try:
                if self.filter_terminal and not entry.getTerminal():
                    continue
                category = entry.getCategories().pop()
                result[category].append(entry)
            except IndexError:
                # HAHA! My past self tought that uncategorized items
                # were not worth it!
                pass
        return result

    def tmux(self, _, what):
        """
            Gets current session
        """
        server = tmuxp.Server()
        cid = "${}".format(os.environ['TMUX'].split(',')[-1])
        session = [s for s in server.sessions if s['session_id'] == cid][0]
        window = session.new_window()
        window.panes[-1].send_keys(what)

    def classic(self, _, what):
        """
            Execute
        """
        return os.system(what)

    @property
    def menu_tree(self):
        """
            Magically build a menu tree.
            This yields curses objects, so here be dragons.
        """
        exit_btn = menu_button('Exit', '', exit_program)

        for menu_category, items in self.categorized_menus.items():
            cat = []
            for item in items:
                cat.append(menu_button(item.getName(), item.getExec(),
                                       self.execute))
            yield sub_menu(menu_category, cat, self.windows)

        yield exit_btn

    def main(self):
        self.windows[0] = CascadingBoxes(menu('Main menu', self.menu_tree))

        urwid.MainLoop(self.windows[0], self.palette).run()


@click.command()
@click.option('--appdir', default="/usr/share/applications/",
              help="Where to find .desktop files")
@click.option('--executor', default='tmux',
              help='How to run selected program',
              type=click.Choice(['tmux', 'classic']))
@click.option('--filter_terminal/--no-filter_terminal', default=True)
def main(appdir=False, executor=False, filter_terminal=True):
    """
        Option management
    """
    if executor == "tmux":
        if not os.environ['TMUX']:
            raise Exception("In order to use tmux integration, "
                            "this must be executed from INSIDE a "
                            "running tmux session")

    return CursedXDG(appdir, executor=executor,
                     filter_terminal=filter_terminal).main()


if __name__ == "__main__":
    main()
