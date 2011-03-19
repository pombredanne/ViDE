from gcc import gcc
from cygwin_gcc import cygwin_gcc
from gcc_test import gcc_test

class cygwin_gcc_test( gcc, cygwin_gcc, gcc_test ):
    pass
