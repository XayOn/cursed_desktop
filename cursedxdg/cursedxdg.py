import os, sys, urwid
from xdg import DesktopEntry

appdir="/usr/share/applications/"

def read_menus():
    """
        Read the menus and return them in an array
    """
    all_menus = []
    result = {}
    for menu_entry_file in os.listdir(appdir):
        if menu_entry_file.endswith('.desktop'):
            all_menus.append(DesktopEntry.DesktopEntry(
                appdir + menu_entry_file
            ))

    for category, ele in [[l.getCategories()[0], l] for l in all_menus if len(l.getCategories()) > 0]:
        if not category in result: result[category] = []
        result[category].append(ele)
    return result

def menu_button(caption, program, callback):
    button = urwid.Button(caption)
    urwid.connect_signal(button, 'click', callback, program)
    return urwid.AttrMap(button, None, focus_map='reversed')

def sub_menu(caption, choices):
    contents = menu(caption, choices)
    def open_menu(button, foo=False):
        return top.open_box(contents)
    return menu_button([caption, ''], False, open_menu)

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    body.extend(choices)
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def exit_program(button, none):
    raise urwid.ExitMainLoop()

def main():
    allmenus = read_menus()
    palette = [
        ('banner', 'black', 'light gray'),
        ('streak', 'black', 'dark red'),
        ('bg', 'black', 'dark blue'),]
    top = CascadingBoxes(menu('Main menu', [sub_menu(menu_category, [menu_button(item.getName(), item.getExec(), lambda foo, x:sys.exit(os.system(x))
    ) for item in allmenus[menu_category] ]) for menu_category in allmenus.keys()] + [menu_button('Exit', False, exit_program)] ))
    urwid.MainLoop(top, palette).run()

class CascadingBoxes(urwid.WidgetPlaceholder):
    max_box_levels = 4

    def __init__(self, box):
        super(CascadingBoxes, self).__init__(urwid.SolidFill())
        self.box_level = 0
        self.open_box(box)

    def open_box(self, box):
        self.original_widget = urwid.Overlay(urwid.LineBox(box),
            self.original_widget,
            align='center', width=('relative', 40),
            valign='middle', height=('relative', 40),
            min_width=24, min_height=8,
            left=self.box_level * 3,
            right=(self.max_box_levels - self.box_level - 1) * 3,
            top=self.box_level * 2,
            bottom=(self.max_box_levels - self.box_level - 1) * 2)
        urwid.AttrMap(self.original_widget, 'bg')

        self.box_level += 1

    def keypress(self, size, key):
        if key == 'esc' and self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1
        else:
            return super(CascadingBoxes, self).keypress(size, key)

if __name__ == "__main__":
    main()
