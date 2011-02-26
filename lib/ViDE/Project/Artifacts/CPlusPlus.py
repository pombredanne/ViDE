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
    def __init__( self, buildkit, localLibraries ):
        self.__buildkit = buildkit
        self.__candidateCopiedHeaders = []
        for lib in localLibraries:
            for copiedHeaders in lib.getCopiedHeaders():
                self.__candidateCopiedHeaders += copiedHeaders.get()

    def find( self, searchedHeader ):
        searchedHeader = self.__buildkit.fileName( "inc", searchedHeader )
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
        self.__parse( headers, self.__source, self.__handleDoubleQuotedHeaderFromDoubleQuotedHeader )
        headers.save( self.__depFile )

    def __parse( self, headers, fileName, handleDoubleQuotedHeader ):
        f = open( fileName )
        for line in f:
            line = line.strip()
            header = self.__doubleQuotedHeaderOnLine( line )
            if header:
                handleDoubleQuotedHeader( headers, fileName, header )
            header = self.__angleHeaderOnLine( line )
            if header:
                self.__handleAngleHeader( headers, header )
        f.close()

    def __handleDoubleQuotedHeaderFromDoubleQuotedHeader( self, headers, fileName, header ):
        header = os.path.join( os.path.dirname( fileName ), header )
        headers.addDoubleQuotedHeader( header )
        self.__parse( headers, header, self.__handleDoubleQuotedHeaderFromDoubleQuotedHeader )

    def __handleDoubleQuotedHeaderFromAngleHeader( self, headers, fileName, header ):
        copiedHeader = self.__candidateCopiedHeaders.find( header )
        headers.addAngleHeader( header )
        self.__parse( headers, copiedHeader.getSource().getFileName(), self.__handleDoubleQuotedHeaderFromAngleHeader )

    def __handleAngleHeader( self, headers, header ):
        copiedHeader = self.__candidateCopiedHeaders.find( header )
        if copiedHeader is not None:
            headers.addAngleHeader( header )
            self.__parse( headers, copiedHeader.getSource().getFileName(), self.__handleDoubleQuotedHeaderFromAngleHeader )

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

    def __init__( self, buildkit, source, candidateCopiedHeaders ):
        fileName = buildkit.fileName( "dep", source.getFileName() + ".dep" )
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
    def __init__( self, buildkit, files, source, localLibraries, explicit ):
        candidateCopiedHeaders = CandidateCopiedHeaders( buildkit, localLibraries )
        headers = self.__parseCppHeaders( buildkit, source, candidateCopiedHeaders )
        includedHeaders = [ Project.inProgress.createArtifact( Header, header, False ) for header in headers.getDoubleQuotedHeaders() ]
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

    def getSource( self ):
        return self.__source

    def __parseCppHeaders( self, buildkit, source, candidateCopiedHeaders ):
        depFile = DepFile( buildkit, source, candidateCopiedHeaders )
        depFile.getProductionAction().execute( False, 1 )
        return Headers.load( depFile.getFileName() )
