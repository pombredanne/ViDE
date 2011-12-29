import sys

from ViDE.Flavour import Flavour

class Release( Flavour ):
    def canBeDefault( self ):
        return False
