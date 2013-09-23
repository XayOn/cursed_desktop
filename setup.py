#!/usr/bin/env python
"""
Setup configuration
"""

from setuptools import find_packages, setup

setup(
    name = 'CursedXDG',
    version = '0.0.1',
    description = 'XDG compliant menu in ncurses',
    url = 'http://github.com/XayOn/CursedXDG',
    keywords = 'xdg python ncurses',
    install_requires = ['pyxdg', 'urwid'],
    entry_points = {
        'console_scripts': ['cursedxdg/cursedxdg.py']},
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
    ],
    author = 'David Francos',
    author_email = 'me@davidfrancos.net',
    maintainer = 'David Francos',
    maintainer_email = 'me@davidfrancos.net',
    download_url = 'http://github.com/XayOn/CursedXDG',
    platforms = ['POSIX'],
    license = 'GPL v3+',
    )
