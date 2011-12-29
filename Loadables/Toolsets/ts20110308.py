from ViDE.Toolset import Toolset

from Tools.PkgConfig import PkgConfig
from Tools.Make import Make
from Tools.LibSigCpp import LibSigCpp
from Tools.Cairo import Pixman, FreeType, FontConfig, LibPng, Cairo, Cairomm, PyCairo

class ts20110308( Toolset ):
    def canBeDefault( self ):
        return False

    def computeTools( self ):
        return [
            Make( "3.82" ),
            PkgConfig( "0.25" ),
            Pixman( "0.20.2" ),
            FreeType( "2.4.4" ),
            FontConfig( "2.8.0" ),
            LibPng( "1.5.1" ),
            Cairo( "1.10.2" ),
            LibSigCpp( "2.2.9" ),
            Cairomm( "1.9.8" ),
            PyCairo( "1.8.10" )
        ]

