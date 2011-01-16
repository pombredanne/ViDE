import os.path
import re

from ViDE.Core.Artifact import AtomicArtifact
from ViDE.Core.Action import Action
from ViDE.Core.Actions import SystemAction

from ViDE.Project import Binary
from ViDE.Project.Project import Project
from ViDE.Project.CPlusPlus.Source import Header

# @todo Implement using Boost.Wave, through Boost.Python
class ParseCppHeadersAction( Action ):
    def __init__( self, source, depFile ):
        Action.__init__( self )
        self.__source = source
        self.__depFile = depFile
        
    def computePreview( self ):
        return "blahblah " + self.__source + " " + self.__depFile
        
    def doExecute( self ):
        headers = self.parse( self.__source )
        f = open( self.__depFile, "w" )
        for header in headers:
            f.write( header + "\n" )
        f.close()
        
    def parse( self, fileName ):
        headers = set()
        f = open( fileName )
        for line in f:
            line = line.strip()
            match = re.match( "\s*#\s*include\s*\"(.*)\"", line )
            if match:
                header = match.groups()[0]
                headers.add( header )
                headers.update( self.parse( header ) )
        f.close()
        return headers

class DepFile( AtomicArtifact ):
    def __init__( self, source ):
        fileName = os.path.join( "build", "dep", source.getFileName() + ".dep" )
        if os.path.exists( fileName ):
            automaticDependencies = [ Header( header.strip() ) for header in open( fileName ) ]
        else:
            automaticDependencies = []
        AtomicArtifact.__init__(
            self,
            name = fileName,
            files = [ fileName ],
            strongDependencies = [ source ],
            orderOnlyDependencies = [],
            automaticDependencies = automaticDependencies
        )
        self.__fileName = fileName
        self.__source = source

    def doGetProductionAction( self ):
        return ParseCppHeadersAction( self.__source.getFileName(), self.__fileName )

    def getFileName( self ):
        return self.__fileName

class Object( Binary.Object ):
    def __init__( self, source, localLibraries ):
        fileName = os.path.join( "build", "obj", source.getFileName() + ".o" )
        headers = self.parseCppHeaders( source )
        Binary.Object.__init__(
            self,
            name = fileName,
            files = [ fileName ],
            strongDependencies = [ source ],
            orderOnlyDependencies = [ lib.getCopiedHeaders() for lib in localLibraries ],
            automaticDependencies = [ Project.inProgress.createOrRetrieve( Header, header ) for header in headers ]
        )
        self.__fileName = fileName
        self.__source = source

    def doGetProductionAction( self ):
        return SystemAction( [ "g++", "-c", "-I" + os.path.join( "build", "inc" ), "-o" + self.__fileName, self.__source.getFileName() ], "g++ -c " + self.__source.getFileName() )

    def getFileName( self ):
        return self.__fileName

    def parseCppHeaders( self, source ):
        depFile = DepFile( source )
        depFile.getProductionAction().execute( False, 1 )
        return [ header.strip() for header in open( depFile.getFileName() ) ]
        