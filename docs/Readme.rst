Cursed_desktop
--------------

Long story short: I really like Text User Interfaces

One of the "modern" improvements commonly found in desktop environments is the applications menu.
FreeDesktop.org defines a fine standard for desktop menu entries, that most distributions and
desktop environments follow, but we don't normally use them in terminal environments.

I frecuently forgot what I have and what it's for, and a menu is really useful for that.
So I wrote one that is compliant (mostly) with the freedesktop's standard and is actually a TUI.

.. note::

    By default, cursed_desktop uses TMUX to handle execution and filters out any non-terminal
    apps. It also uses /usr/share/applications directory


You may even build your own menu just by changing the .desktop directory to one of your own making 
that follows the standard..


Here, an example (a bit outdated, right now cursed_desktop handles format strings in .desktop files)

.. image:: /docs/cursed_desktop.gif?raw=true


Features
--------

* Freedesktop.org .desktop file compliant
* Tmux integration

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
