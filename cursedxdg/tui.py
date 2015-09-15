#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urwid

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

"""


def menu_button(caption, program, callback):
    button = urwid.Button(caption)
    urwid.connect_signal(button, 'click', callback, program)
    return urwid.AttrMap(button, None, focus_map='reversed')


def sub_menu(caption, choices, windows):
    contents = menu(caption, choices)

    def open_menu(button, foo=False):
        return windows[0].open_box(contents)

    return menu_button([caption, ''], False, open_menu)


def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    body.extend(choices)
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


def exit_program(button, none):
    raise urwid.ExitMainLoop()


class CascadingBoxes(urwid.WidgetPlaceholder):
    max_box_levels = 4

    def __init__(self, box):
        super(CascadingBoxes, self).__init__(urwid.SolidFill())
        self.box_level = 0
        self.open_box(box)

    def open_box(self, box):
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
        if key == 'esc' and self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1
        else:
            return super(CascadingBoxes, self).keypress(size, key)
