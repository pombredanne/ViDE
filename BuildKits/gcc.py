import os

from ViDE.BuildKit.Description import *

class GccCompiler:
    def getFiles( self, sourceName ):
        return [ os.path.join( "build", "obj", sourceName + ".o" ) ]
    
    def getSystem( self, sourceName ):
        return [ "g++", "-c", "-I" + os.path.join( "build", "inc" ), "-o" + self.getFiles( sourceName )[ 0 ], sourceName ]

Compiler( GccCompiler() )
