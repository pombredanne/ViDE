import os.path
import itertools
import fnmatch

from Misc import InteractiveCommandLineProgram as ICLP

import ViDE

class CheckImports( ICLP.Command ):
    def walkDirectory( self, directory ):
        for path, dirs, files in os.walk( directory ):
            for fileName in fnmatch.filter( files, "*.py" ):
                yield os.path.join( path, fileName )

    def allFiles( self ):
        return itertools.chain( 
            self.walkDirectory( os.path.join( ViDE.rootDirectory(), "lib" ) ),
            self.walkDirectory( os.path.join( ViDE.rootDirectory(), "BuildKits" ) ),
            self.walkDirectory( os.path.join( ViDE.rootDirectory(), "TestProjects" ) ),
            self.walkDirectory( os.path.join( ViDE.rootDirectory(), "ToolSets", "Tools" ) ),
        )

    def execute( self, args ):
        for f in self.allFiles():
            used = dict()
            for line in open( f ):
                line = line.strip()
                if line.find( "import " ) != -1:
                    self.addSymbols( line, used )
                else:
                    self.useSymbols( line, used )
            for symbol in used:
                if not used[ symbol ]:
                    print f + ": unused symbol", symbol

    def addSymbols( self, line, used ):
        imports = line[ line.find( "import" )+7: ]
        symbols = [ symbol.split( "as" )[-1].strip() for symbol in imports.split( "," ) ]
        for symbol in symbols:
            if symbol not in ( "*", "with_statement", '" ) != -1:' ):
                used[ symbol ] = False

    def useSymbols( self, line, used ):
        for symbol in used:
            if line.find( symbol ) != -1:
                used[ symbol ] = True
