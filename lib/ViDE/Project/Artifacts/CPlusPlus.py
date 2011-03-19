import os.path
import re
import sys
import itertools

from ViDE.Core.Artifact import AtomicArtifact, InputArtifact
from ViDE.Core.Action import Action
from ViDE.Project.Project import Project
from ViDE.Project.Artifacts.BasicArtifacts import MonofileInputArtifact

class Header( MonofileInputArtifact ):
    pass

class Source( MonofileInputArtifact ):
    pass

class CandidateCopiedHeaders:
    def __init__( self, context, localLibraries ):
        self.context = context
        self.__candidateCopiedHeaders = []
        for lib in localLibraries:
            for copiedHeaders in lib.getCopiedHeaders():
                self.__candidateCopiedHeaders += copiedHeaders.get()

    def find( self, searchedHeader ):
        searchedHeader = self.context.buildkit.fileName( "inc", searchedHeader )
        for copiedHeader in self.__candidateCopiedHeaders:
            if searchedHeader == copiedHeader.getDestination():
                return copiedHeader

class Headers:
    def __init__( self ):
        self.__doubleQuotedHeaders = set()
        self.__angleHeaders = set()

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
        self.__doubleQuotedHeaders.add( header )

    def addAngleHeader( self, header ):
        self.__angleHeaders.add( header )

# @todo Implement using Boost.Wave, through Boost.Python
class ParseCppHeadersAction( Action ):
    def __init__( self, source, depFile, candidateCopiedHeaders ):
        Action.__init__( self )
        self.__source = source
        self.__depFile = depFile
        self.__candidateCopiedHeaders = candidateCopiedHeaders

    def computePreview( self ):
        return "blahblah " + self.__source + " " + self.__depFile

    def doExecute( self ):
        headers = Headers()
        self.__parse( headers, self.__source, self.__handleDoubleQuotedHeaderFromDoubleQuotedHeader, "" )
        headers.save( self.__depFile )

    def __parse( self, headers, fileName, handleDoubleQuotedHeader, path ):
        f = open( fileName )
        for line in f:
            line = line.strip()
            header = self.__doubleQuotedHeaderOnLine( line )
            if header:
                handleDoubleQuotedHeader( headers, fileName, header, path )
            header = self.__angleHeaderOnLine( line )
            if header:
                self.__handleAngleHeader( headers, header, path )
        f.close()

    def __handleDoubleQuotedHeaderFromDoubleQuotedHeader( self, headers, fileName, header, path ):
        header = os.path.join( os.path.dirname( fileName ), header )
        headers.addDoubleQuotedHeader( header )
        self.__parse( headers, header, self.__handleDoubleQuotedHeaderFromDoubleQuotedHeader, path )

    def __handleDoubleQuotedHeaderFromAngleHeader( self, headers, fileName, header, path ):
        header = os.path.join( path, header )
        copiedHeader = self.__candidateCopiedHeaders.find( header )
        headers.addAngleHeader( header )
        self.__parse( headers, copiedHeader.getSource().getFileName(), self.__handleDoubleQuotedHeaderFromAngleHeader, path )

    def __handleAngleHeader( self, headers, header, path ):
        copiedHeader = self.__candidateCopiedHeaders.find( header )
        if copiedHeader is not None:
            headers.addAngleHeader( header )
            self.__parse( headers, copiedHeader.getSource().getFileName(), self.__handleDoubleQuotedHeaderFromAngleHeader, os.path.join( path, os.path.dirname( header )  ) )

    def __doubleQuotedHeaderOnLine( self, line ):
        return self.__headerOnLine( line, "\s*#\s*include\s*\"(.*)\"" )

    def __angleHeaderOnLine( self, line ):
        return self.__headerOnLine( line, "\s*#\s*include\s*<(.*)>" )

    def __headerOnLine( self, line, regex ):
        match = re.match( regex, line )
        if match:
            return match.groups()[0]
        else:
            return None

class DepFile( AtomicArtifact ):
    class Header( InputArtifact ):
        def __init__( self, header ):
            InputArtifact.__init__(
                self,
                name = header,
                files = [ header ],
                explicit = False
            )

    def __init__( self, context, source, candidateCopiedHeaders ):
        fileName = context.buildkit.fileName( "dep", source.getFileName() + ".dep" )
        if os.path.exists( fileName ):
            headers = Headers.load( fileName )
            automaticDependencies = [ DepFile.Header( header ) for header in headers.getDoubleQuotedHeaders() ]
            for searchedHeader in headers.getAngleHeaders():
                automaticDependencies.append( DepFile.Header( candidateCopiedHeaders.find( searchedHeader ).getSource().getFileName() ) )
        else:
            automaticDependencies = []
        AtomicArtifact.__init__(
            self,
            name = fileName,
            files = [ fileName ],
            strongDependencies = [ source ],
            orderOnlyDependencies = [],
            automaticDependencies = automaticDependencies,
            explicit = False
        )
        self.__fileName = fileName
        self.__source = source
        self.__candidateCopiedHeaders = candidateCopiedHeaders

    def doGetProductionAction( self ):
        return ParseCppHeadersAction( self.__source.getFileName(), self.__fileName, self.__candidateCopiedHeaders )

    def getFileName( self ):
        return self.__fileName

class Object( AtomicArtifact ):
    def __init__( self, context, files, source, localLibraries, externalLibraries, explicit ):
        self.context = context
        candidateCopiedHeaders = CandidateCopiedHeaders( context, localLibraries )
        headers = self.__parseCppHeaders( context, source, candidateCopiedHeaders )
        includedHeaders = [ self.__retrieveOrCreateHeader( header ) for header in headers.getDoubleQuotedHeaders() ]
        for searchedHeader in headers.getAngleHeaders():
            includedHeaders.append( candidateCopiedHeaders.find( searchedHeader ) )
        AtomicArtifact.__init__(
            self,
            name = files[ 0 ],
            files = files,
            strongDependencies = [ source ],
            orderOnlyDependencies = list( itertools.chain.from_iterable( lib.getCopiedHeaders() for lib in localLibraries ) ),
            automaticDependencies = includedHeaders,
            explicit = explicit
        )
        self.__source = source
        self.__externalLibraries = externalLibraries

    def getSource( self ):
        return self.__source

    def __retrieveOrCreateHeader( self, header ):
        artifact = Project.inProgress.retrieveByName( header )
        if artifact is None:
            artifact = Project.inProgress.createArtifact( Header, header, False )
        return artifact

    def __parseCppHeaders( self, context, source, candidateCopiedHeaders ):
        depFile = DepFile( context, source, candidateCopiedHeaders )
        depFile.getProductionAction().execute( False, 1 )
        return Headers.load( depFile.getFileName() )

    def getIncludeDirectories( self ):
        directories = []
        for lib in self.__externalLibraries:
            directories += self.context.toolset.getTool( lib ).getIncludeDirectories( self.context )
        return directories

    def getLibrariesToLink( self ):
        return [ self.context.toolset.getTool( lib ) for lib in self.__externalLibraries ]
