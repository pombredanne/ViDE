import os

from ViDE.Toolset import Tool

class Python( Tool ):
    def getDependencies( self ):
        return []

    def getIncludeDirectories( self, context ):
        return [ os.path.join( context.toolset.getInstallDirectory(), *path ) for path in [
            ( "include", "python2.7" )
        ] ]

    def getLibPath( self ):
        return "/home/Vincent/Programmation/ViDE/Toolsets/Install/ts20110308/lib"

    def getLibName( self ):
        return "python2.7"
