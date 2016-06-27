Cursed Desktop
--------------

A simple ncurses system menu

.. image:: https://img.shields.io/github/downloads/xayon/cursed_desktop/total.svg?maxAge=2592000
.. image:: https://img.shields.io/pypi/dm/cursed_desktop.svg?maxAge=2592000
.. image:: https://img.shields.io/github/stars/badges/shields.svg?style=social&label=Star&maxAge=2592000

.. image:: /docs/cursed_desktop.gif?raw=true

One of the "modern" improvements commonly found in desktop environments is the applications menu.
FreeDesktop.org defines a fine standard for desktop menu entries, that most distributions and
desktop environments follow, but we don't normally use them in terminal environments.

I frecuently forgot what I have and what it's for, and a menu is really useful for that.
So I wrote one that is compliant (mostly) with the freedesktop's standard and is actually a TUI.


::

    By default, cursed_desktop uses TMUX to handle execution and filters out any non-terminal
    apps. It also uses /usr/share/applications directory


Features
--------

* Freedesktop.org .desktop file compliant
* Tmux integration

You may even build your own menu just by changing the .desktop directory to one of your own making
that follows the standard.

Usage
-----

::

    Usage: cursed_desktop [OPTIONS]

      Options:
        --appdir TEXT                   Where to find .desktop files
        --executor [tmux|classic]       How to run selected program
        --filter_terminal / --no-filter_terminal
        --help                          Show this message and exit.


Just running cursed_desktop without options should be fine for most people.

Note
----

Please, if you use this, put a star on it / interact with an
issue if you have a problem / send me an email.
I'll be very happy to know there are people out there at least as
mad as myself.

This project requires very little maintainment for my personal use
but I'll be happy to give it a bit more love if you guys support it.
