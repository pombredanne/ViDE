from ViDE.Toolset import Toolset

from Tools.PkgConfig import PkgConfig
from Tools.Make import Make
from Tools.LibSigCpp import LibSigCpp
from Tools.Python import Python
from Tools.Cairo import Pixman, FreeType, FontConfig, LibPng, Cairo, Cairomm, PyCairo
from Tools.Boost import BoostPython, BoostUnitTestFramework, BoostProgramOptions
from Tools.Win32 import Gdi

class system( Toolset ):
    def computeTools( self ):
        return [
            Make( "system" ),
            PkgConfig( "system" ),
            Pixman( "system" ),
            FreeType( "system" ),
            FontConfig( "system" ),
            LibPng( "system" ),
            Cairo( "system" ),
            LibSigCpp( "system" ),
            Cairomm( "system" ),
            Python( "system" ),
            PyCairo( "system" ),
            BoostPython( "system" ),
            BoostProgramOptions( "system" ),
            BoostUnitTestFramework( "system" ),
            Gdi( "system" )
        ]

    def getInstallDirectory( self ):
        return "/usr"
