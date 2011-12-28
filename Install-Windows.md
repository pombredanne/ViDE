This document details how to install ViDE and its dependencies so that it is usable from three shells: the Windows command prompt, Cygwin's bash, and MSys.

The basic idea is that Cygwin is a standalone system that uses its own version of most tools and libraries, while MSys aims at being very Windows-compatible.
The only tools for which we will not install a Cywgin version, and let Cygwin call the Windows version, are executable tools that will not be linked to our own programs: Git and Graphviz.
Beside that, all other tools (Python, Gtk, Cairo, etc.) will have two versions: one for Cygwin, and one for Windows. Some of them will even have two versions for Windows, if Visual Studio and MinGW are incompatible.

Dependencies for Windows, Cygwin and MinGW/MSys
===============================================

Git
---

- Download and launch `Git-X.X.X.X-previewXXXXXXXX.exe` from [MsysGit](http://code.google.com/p/msysgit/downloads/list)
    - in "Select Components", unselect all options unless you have special needs
    - in "Adjusting your PATH environment", select "Run Git from the Windows Command Prompt"
    - in "Configuring the line ending conversions", select "Checkout as-is, commit as-is"
- From the Windows command prompt, run `git config --global user.name "Your Name"`
- From the Windows command prompt, run `git config --global user.email you@yourdomain.com`

Graphviz
--------

- Download and launch `graphviz-X.XX.X.msi` from [Graphviz](http://graphviz.org/Download.php)

Dependencies for Windows and MinGW/MSys
=======================================

Python
------

- Download and launch `python-2.X.X.msi` from [Python](http://python.org/download/) (Stick to a 2.X 32bits version because some extensions used do not support 3.X or 64bits)
- Download and launch `setuptools-X.XXXX.win32-py2.X.exe` from [Setup tools](http://pypi.python.org/pypi/setuptools)
- Download and launch `pygtk-all-in-one-X.XX.0.win32-py2.X.msi` from [PyGtk](http://ftp.gnome.org/pub/GNOME/binaries/win32/pygtk/)
    - Select every optional components
- **To be confirmed:** Add `c:\Python27` and `c:\Python27\Scripts` to your PATH environment variable
- From the Windows command prompt, run `easy_install odict markdown django`

Visual Studio Express
---------------------

ViDE
====

- From the Windows command prompt, run `git clone git@github.com:jacquev6/ViDE.git`
- Add `ViDE\bin` to your system PATH environment variable

Cygwin
======

Packaged software
-----------------

- Download setup.exe from [Cygwin](http://www.cygwin.com/), copy it to a new dircetory c:\cygwin, and launch it
    - in "Select Local Package Directory", choose `c:\cygwin\LocalPackages`
    - in "Select packages", select at least:
        - wget
        - make, m4, pkg-config
        - libsigc-2.0_0, libsigc-2.0-devel
        - python, python-gtk2.0, python-gtk2.0-devel, libgtk2.0-devel
        - libboost-devel
        - gcc4-fortran
- In file `c:\cygwin\etc\passwd`, change your home directory from `/home/username` to `/cygdrive/c/Users/username`

Non-packaged software
---------------------

### Cairomm

- Download `cairomm-X.XX.X.tar.gz` from [Cairo](http://cairographics.org/releases/)
- From Cygwin, run `tar xzf cairomm-X.XX.X.tar.gz`, then `cd cairomm-X.XX.X; ./configure; make; make install`

### Python modules

- From Cygwin, run `wget http://peak.telecommunity.com/dist/ez_setup.py` and `python ez_setup.py`
- From Cygwin, run `easy_install odict markdown django`

### Xming X server

- Download and launch `Xming-X-X-X-XX-setup.exe` from [XMing](http://sourceforge.net/projects/xming/)
    - in "Select Components", choose "Don't install an SSH client"
- In file `c:\cygwin\cygwin.bat`, add a line `set DISPLAY=127.0.0.1:0` (before the line calling bash)

MinGW/MSys
==========

- Download and launch `mingw-get-inst-XXXXXXXX.exe` from [MinGW](http://sourceforge.net/projects/mingw/files)
	- in "Select Components", select all options
- In file `C:\MinGW\msys\1.0\etc\profile`, modify the "Set up USER's home directory" section to set the HOME environment variable to `"/c/Users/username"` instead of `"/home/$LOGNAME"`
