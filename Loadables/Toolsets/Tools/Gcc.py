from ViDE.Toolset import Tool

# ftp://ftp.gnu.org/gnu/gcc/gcc-4.6.0/gcc-4.6.0.tar.bz2
# http://www.mpfr.org/mpfr-current/mpfr-3.0.0.tar.bz2
# http://www.multiprecision.org/mpc/download/mpc-0.9.tar.gz

class Gcc( Tool ):
    def getDependencies( self ):
        return []

