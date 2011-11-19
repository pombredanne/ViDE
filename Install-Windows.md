This document details how to install ViDE and its dependencies so that it is usable from three shells: the Windows command prompt, Cygwin's bach, and MSys.

Windows command prompt
======================

Cygwin
======

Installation:
- Download setup.exe from http://www.cygwin.com/, copy it to a new dircetory c:\cygwin, and launch it
    - in "Select Local Package Directory", choose c:\cygwin\LocalPackages
    - in "Select packages", select at least:
        - wget
        - make, m4
        - python, python-gtk2.0, python-gtk2.0-devel, libgtk2.0-devel
        - libboost-devel
- From Cygwin, run `wget http://peak.telecommunity.com/dist/ez_setup.py` and `python ez_setup.py`
- From Cygwin, run `easy_install odict markdown django`
- Download and launch Xming-X-X-X-XX-setup.exe from http://sourceforge.net/projects/xming/
    - in "Select Components", choose "Don't install an SSH client"
- In file c:\cygwin\cygwin.bat, add a line `set DISPLAY=127.0.0.1:0` (before the line calling bash)

Check:
- From Cygwin, run `python --version`, `easy_install --help` and `python -c "import pygtk, gtk, odict, markdown, django"`

MinGW/MSys
==========

Installation:
- Download and launch mingw-get-inst-XXXXXXXX.exe from http://sourceforge.net/projects/mingw/files
	- in "Select Components", select all options
- In file C:\MinGW\msys\1.0\etc\profile, modify the "Set up USER's home directory" section to set the HOME environment variable to "$USERPROFILE" instead of "/home/$LOGNAME"

Dependencies for Windows, Cygwin and MinGW/MSys
===============================================

Git
---

Installation:
- Download and launch Git-X.X.X.X-previewXXXXXXXX.exe from http://code.google.com/p/msysgit/
    - in "Select Components", unselect all options unless you have special needs
    - in "Adjusting your PATH environment", select "Run Git from the Windows Command Prompt"
    - in "Configuring the line ending conversions", select "Checkout as-is, commit as-is"
- From the Windows command prompt, run `git config --global user.name "Your Name"`
- From the Windows command prompt, run `git config --global user.email you@yourdomain.com`

Check:
- From the Windows command prompt, run `git --version`

Graphviz
--------

Installation:
- Download and launch graphviz-X.XX.X.msi from http://graphviz.org/

Check:
- From the three shells, run `dot -V`

ViDE
====

Installation:
- From the Windows command prompt, run `git clone git@github.com:jacquev6/ViDE`
- Add ViDE\bin to your system PATH environment variable

Check:
- From the three shells, run `git --version` and `vide help`

Dependencies for Windows and MinGW/MSys
=======================================

Python for Windows
------------------

Installation:
- Download and launch python-2.X.X.msi from http://python.org (Stick to a 2.X 32bits version because some extensions used do not support 3.X or 64bits)
- Download and launch setuptools-X.XXXX.win32-py2.X.exe from http://pypi.python.org/pypi/setuptools
    - Select every optional components
- Download and launch pygtk-all-in-one-X.XX.0.win32-py2.X.msi from http://ftp.gnome.org/pub/GNOME/binaries/win32/pygtk/
========>>>>>> - Add c:\Python27 and c:\Python27\Scripts to your PATH environment variable
- From the Windows command prompt, run `easy_install odict markdown django`

Check:
- From the three shells, run `python --version`, `easy_install --help` and `python -c "import pygtk, gtk, odict, markdown, django"`

Visual Studio Express
---------------------
