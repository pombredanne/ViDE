import os.path
import re

from ViDE.Core.Artifact import AtomicArtifact
from ViDE.Core.Action import Action

from ViDE.Project.Project import Project
from ViDE.Project.CPlusPlus.Source import Header

class Headers:
    def __init__( self ):
        self.__doubleQuotedHeaders = []
        self.__angleHeaders = [ "lib.hpp" ]
        
    def save( self, fileName ):
        f = open( fileName, "w" )
        for header in self.__doubleQuotedHeaders:
            f.write( header + "\n" )
        f.close()
    
    @staticmethod
    def load( fileName ):
        headers = Headers()
        for header in open( fileName ):
            headers.addDoubleQuotedHeader( header.strip() )
        return headers
    
    def getDoubleQuotedHeaders( self ):
        return self.__doubleQuotedHeaders
    
    def getAngleHeaders( self ):
        return self.__angleHeaders
        
    def addDoubleQuotedHeader( self, header ):
        self.__doubleQuotedHeaders.append( header )
    
    def addAngleHeader( self, header ):
        self.__angleHeaders.append( header )

# @todo Implement using Boost.Wave, through Boost.Python
class ParseCppHeadersAction( Action ):
    def __init__( self, source, depFile ):
        Action.__init__( self )
        self.__source = source
        self.__depFile = depFile
        
    def computePreview( self ):
        return "blahblah " + self.__source + " " + self.__depFile
        
    def doExecute( self ):
        headers = Headers()
        for header in self.parse( self.__source ):
            headers.addDoubleQuotedHeader( header )
        headers.save( self.__depFile )
        
    def parse( self, fileName ):
        headers = set()
        f = open( fileName )
        for line in f:
            line = line.strip()
            ### @todo Handle <...> includes for local libraries => copy library headers before anything: NO: just continue exploration in the headers of the local libraries
            match = re.match( "\s*#\s*include\s*\"(.*)\"", line )
            if match:
                header = match.groups()[0]
                headers.add( header )
                headers.update( self.parse( header ) )
        f.close()
        return headers

class DepFile( AtomicArtifact ):
    def __init__( self, buildkit, source, localLibraries ):
        fileName = buildkit.fileName( "dep", source.getFileName() + ".dep" )
        if os.path.exists( fileName ):
            headers = Headers.load( fileName )
            automaticDependencies = [ Header( buildkit, header ) for header in headers.getDoubleQuotedHeaders() + headers.getAngleHeaders() ]
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

class Object( AtomicArtifact ):
    def __init__( self, buildkit, files, source, localLibraries ):
        headers = self.parseCppHeaders( buildkit, source, localLibraries )
        copiedHeaders = []
        AtomicArtifact.__init__(
            self,
            name = files[ 0 ],
            files = files,
            strongDependencies = [ source ],
            orderOnlyDependencies = [ lib.getCopiedHeaders() for lib in localLibraries ],
            automaticDependencies =
                [ Project.inProgress.createOrRetrieve( Header, header ) for header in headers.getDoubleQuotedHeaders() ]
                + copiedHeaders
                # + [ Project.inProgress.retrieveByName( CopiedHeader, header ) for header in headers.getAngleHeaders() ]
        )
        self.__source = source

    def getSource( self ):
        return self.__source

    def parseCppHeaders( self, buildkit, source, localLibraries ):
        depFile = DepFile( buildkit, source, localLibraries )
        depFile.getProductionAction().execute( False, 1 )
        return Headers.load( depFile.getFileName() )
