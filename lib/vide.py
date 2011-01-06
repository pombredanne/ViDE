import sys

from ViDE.Shell.Shell import Shell

if __name__ == "__main__":
    Shell().execute( [ "vide" ] + sys.argv[ 1: ] )
