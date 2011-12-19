import ViDE
from ViDE.Toolset import Toolset

from Tools.PkgConfig import PkgConfig
from Tools.Make import Make
from Tools.LibSigCpp import LibSigCpp
from Tools.Python import Python
from Tools.Cairo import Pixman, FreeType, FontConfig, LibPng, Cairo, Cairomm, PyCairo
from Tools.Boost import BoostPython, BoostUnitTestFramework, BoostProgramOptions, BoostThread, BoostDateTime, BoostSystem, BoostFileSystem
from Tools.Win32 import Gdi
from Tools.Pcap import Pcap

class system( Toolset ):
    def canBeDefault( self ):
        return True

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
            Gdi( "system" ),
            BoostThread( "system" ),
            BoostDateTime( "system" ),
            BoostSystem( "system" ),
            BoostFileSystem( "system" ),
            Gdi( "system" ),
            Pcap( "system"),
        ]

    def getInstallDirectory( self ):
        ### @todo Add a notion of Host and Target. Buildkits make the link between hosts and targets
        host = ViDE.host()
        if host == "cygwin":
            return "/usr"
        elif host == "win32":
            return "c:\\Python27\\"
        elif host == "linux":
            return "/usr"
        else:
            raise Exception( "System Buildkit not ready for host " + host )
