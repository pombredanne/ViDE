import os
import sys

import ViDE
from ViDE.Toolset import Tool

class Python( Tool ):
    versionName = "python" + str( sys.version_info[ 0 ] ) + "." + str( sys.version_info[ 1 ] )

    def getDependencies( self ):
        return []

    def getIncludeDirectories( self, context ):
        return [ os.path.join( context.toolset.getInstallDirectory(), *path ) for path in [
            ( "include", Python.versionName ),
            ( "include", )
        ] ]

    def getLibPath( self ):
        if ViDE.host() == "win32":
            return "c:\\Python27\\libs"
        else:
            return None

    def getLibName( self ):
        if ViDE.host() == "win32":
            return "python27"
        else:
            return Python.versionName
