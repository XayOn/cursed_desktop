#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Ncurses stuffs are always ugly.

    So... this goes here, hopefully unnoticed by most people.

                 __________/%%%%=
                /%%%%%%%%%/%%%%=
          =/%%%/%%%%%%%%%/%%%%=
         =/%%%/%%%%%%%%%/%%%%=
        =/%%%/%%%%%%%%%/%%%%=
       =/%%%/%%%%%%%%%/%%%%=
      =/%%%/%%%%%%%%%/
     =/%%%/

    (a carpet, got from: http://www.retrojunkie.com/asciiart/myth/carpets.htm )
    (Yes, that is a terrible joke about me hiding things under the carpet)

    Apparently my past me decided max_box_levels was going to be 4 by default.
    Have that in mind if you intend to use this code for anything useful
    that is not a normal menu based on xdg (wich usually should be around 3
    levels)

    Oh! Cool, after documenting and re-learning what this does, it's actually
    not so bad.
"""
import urwid


def menu_button(caption, program, callback):
    """
        Generate a menu button and assign it to a callback.
        That is, in this case either:
            - A call to current exec stuff
            - A submenu change
    """
    button = urwid.Button(caption)
    urwid.connect_signal(button, 'click', callback, program)
    return urwid.AttrMap(button, None, focus_map='reversed')


def sub_menu(caption, choices, windows):
    """
        Submenu, it creates a menu, and a button to open
        it with a callback.
    """
    contents = menu(caption, choices)

    def open_menu(button, _=False):
        """
            Ta-Da!
        """
        return windows[0].open_box(contents)

    return menu_button([caption, ''], False, open_menu)


def menu(title, choices):
    """
        Main menu.
    """
    body = [urwid.Text(title), urwid.Divider()]
    body.extend(choices)
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


def exit_program(button=False, _=False):
    """
        GTFO
    """
    raise urwid.ExitMainLoop()


class CascadingBoxes(urwid.WidgetPlaceholder):
    """
        Main placeholder
    """
    max_box_levels = 4

    def __init__(self, box):
        super(CascadingBoxes, self).__init__(urwid.SolidFill())
        self.box_level = 0
        self.open_box(box)

    def open_box(self, box):
        """
           Some magic happens here.
           It opens a box, with a lot of hardcoded + calculated
           positions, relative to previous open box.
           Once we close a box, we decrement the current box count.
           This way we get a nice "animation" on cascading windows
           (hence the class name)
        """
        self.original_widget = urwid.Overlay(
            urwid.LineBox(box),
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
        """
            Override default keypress so we can close cascading boxes AND
            decrement current box level
        """
        if key == 'esc' and self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1
        elif key == "esc" and self.box_level == 1:
            exit_program()
        else:
            super(CascadingBoxes, self).keypress(size, key)


def has_formatters(what):
    """
        Checks if has any formatters
    """
    safely_removed = [r'%k', r'%c', r'%i']

    for key in safely_removed:
        what = what.replace(key, '')

    if '%' not in what:
        return False

    if what.count('%') != 1:
        raise Exception('Multiple formatters are not currently supported')

    return True


def format_(what, val):
    """
        Handles freedesktop's entry spec exec format modifiers
        As described in the desktop entry spec:
        http://standards.freedesktop.org/desktop-entry-spec/latest/ar01s06.html
    """

    safely_removed = [r'%k', r'%c', r'%i']

    for key in safely_removed:
        what = what.replace(key, '')

    all_keys = [r'%f', '%u', r'%F', '%U']
    multi = [r'%F', '%U']

    for key in all_keys:
        if key in what:
            if key not in multi:
                # Acording to the spec, multiple files in single formatters
                # must be dealt with by the implementations...
                val = val.split()[0]
            return what.replace(key, val)

    return what
