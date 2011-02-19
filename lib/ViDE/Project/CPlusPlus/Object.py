import os.path
import re
import sys

from ViDE.Core.Artifact import AtomicArtifact
from ViDE.Core.Action import Action

from ViDE.Project.Project import Project
from ViDE.Project.CPlusPlus.Source import Header

class Headers:
    def __init__( self ):
        self.__doubleQuotedHeaders = []
        self.__angleHeaders = []
        
    def save( self, fileName ):
        f = open( fileName, "w" )
        for header in self.__doubleQuotedHeaders:
            f.write( header + "\n" )
        f.write( "\n" )
        for header in self.__angleHeaders:
            f.write( header + "\n" )
        f.close()
    
    @staticmethod
    def load( fileName ):
        headers = Headers()
        adder = headers.addDoubleQuotedHeader
        for header in open( fileName ):
            header = header.strip()
            if header == "":
                adder = headers.addAngleHeader
            else:
                adder( header.strip() )
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
        self.parse( headers, self.__source )
        headers.save( self.__depFile )
        
    def parse( self, headers, fileName ):
        f = open( fileName )
        for line in f:
            line = line.strip()
            match = re.match( "\s*#\s*include\s*\"(.*)\"", line )
            if match:
                header = match.groups()[0]
                headers.addDoubleQuotedHeader( header )
                self.parse( headers, header )
            else:
                match = re.match( "\s*#\s*include\s*<(.*)>", line )
                if match:
                    header = match.groups()[0]
                    headers.addAngleHeader( header )
        f.close()

class DepFile( AtomicArtifact ):
    def __init__( self, buildkit, source, localLibraries ):
        fileName = buildkit.fileName( "dep", source.getFileName() + ".dep" )
        if os.path.exists( fileName ):
            headers = Headers.load( fileName )
            automaticDependencies = [ Header( buildkit, header ) for header in headers.getDoubleQuotedHeaders() ]
            allCopiedHeaders = []
            ### @todo Factorize with Object.__init__
            for lib in localLibraries:
                allCopiedHeaders += lib.getCopiedHeaders()
            for searchedHeader in headers.getAngleHeaders():
                for copiedHeaders in allCopiedHeaders:
                    for copiedHeader in copiedHeaders.get():
                        if buildkit.fileName( "inc", searchedHeader ) == copiedHeader.getDestination():
                            automaticDependencies.append( Header( buildkit, copiedHeader.getSource().getFileName() ) )
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
        automaticDependencies = [ Project.inProgress.createOrRetrieve( Header, header ) for header in headers.getDoubleQuotedHeaders() ]
        orderOnlyDependencies = []
        for lib in localLibraries:
            orderOnlyDependencies += lib.getCopiedHeaders()
        for searchedHeader in headers.getAngleHeaders():
            for copiedHeaders in orderOnlyDependencies:
                for copiedHeader in copiedHeaders.get():
                    if buildkit.fileName( "inc", searchedHeader ) == copiedHeader.getDestination():
                        automaticDependencies.append( copiedHeader )
        AtomicArtifact.__init__(
            self,
            name = files[ 0 ],
            files = files,
            strongDependencies = [ source ],
            orderOnlyDependencies = orderOnlyDependencies,
            automaticDependencies = automaticDependencies
        )
        self.__source = source

    def getSource( self ):
        return self.__source

    def parseCppHeaders( self, buildkit, source, localLibraries ):
        depFile = DepFile( buildkit, source, localLibraries )
        depFile.getProductionAction().execute( False, 1 )
        return Headers.load( depFile.getFileName() )
