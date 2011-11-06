import os
import sys

from ViDE.Toolset import Tool

class Python( Tool ):
    versionName = "python" + str( sys.version_info[ 0 ] ) + "." + str( sys.version_info[ 1 ] )

    def getDependencies( self ):
        return []

    def getIncludeDirectories( self, context ):
        return [ os.path.join( context.toolset.getInstallDirectory(), *path ) for path in [
            ( "include", Python.versionName )
        ] ]

    def getLibPath( self ):
        return "/home/Vincent/Programmation/ViDE/Toolsets/Install/ts20110308/lib"

    def getLibName( self ):
        return Python.versionName
