import os

from ViDE.BuildKit.Description import *

class GccCompiler:
    def getFiles( self, sourceName ):
        return [ os.path.join( "build", "obj", sourceName + ".o" ) ]

Compiler( GccCompiler() )
