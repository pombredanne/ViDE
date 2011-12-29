from gcc import gcc
from cygwin_gcc import cygwin_gcc
from gcc_release import gcc_release

class cygwin_gcc_release( gcc, cygwin_gcc, gcc_release ):
    pass
