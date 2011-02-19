import os.path

from ViDE.Core.Actions import CopyFileAction
from ViDE.Core.Artifact import AtomicArtifact, CompoundArtifact

class CopiedHeader( AtomicArtifact ):
    def __init__( self, buildkit, header ):
        self.__header = header
        self.__copiedHeader = buildkit.fileName( "inc", header.getFileName() )
        AtomicArtifact.__init__(
            self,
            name = self.__copiedHeader,
            files = [ self.__copiedHeader ],
            strongDependencies = [ header ],
            orderOnlyDependencies = [],
            automaticDependencies = []
        )

    def doGetProductionAction( self ):
        return CopyFileAction( self.__header.getFileName(), self.__copiedHeader )

class CopiedHeaders( CompoundArtifact ):
    def __init__( self, buildkit, name, headers ):
        copiedHeaders = [ CopiedHeader( buildkit, header ) for header in headers ]
        CompoundArtifact.__init__( self, name = name + "_hdr", componants = copiedHeaders )

class Library( CompoundArtifact ):
    @staticmethod
    def computeName( buildkit, name, headers, binary, localLibraries ):
        return "lib" + name

    def __init__( self, buildkit, name, headers, binary, localLibraries ):
        self.__libName = name
        self.__copiedHeaders = CopiedHeaders( buildkit, name, headers )
        self.__binary = binary
        self.__localLibraries = localLibraries
        componants = [ self.__copiedHeaders ]
        if binary is not None:
            componants.append( binary )
        CompoundArtifact.__init__(
            self,
            name = "lib" + name,
            componants = componants
        )

    def getLibName( self ):
        return self.__libName

    def getCopiedHeaders( self ):
        copiedHeaders = [ self.__copiedHeaders ]
        for lib in self.__localLibraries:
            copiedHeaders += lib.getCopiedHeaders()
        return copiedHeaders

    def getBinary( self ):
        return self.__binary

    def getLocalLibraries( self ):
        return self.__localLibraries

class HeaderLibrary( Library ):
    @staticmethod
    def computeName( buildkit, name, headers, localLibraries ):
        return Library.computeName( buildkit, name, headers, None, localLibraries )

    def __init__( self, buildkit, name, headers, localLibraries ):
        Library.__init__(
            self,
            buildkit = buildkit,
            name = name,
            headers = headers,
            binary = None,
            localLibraries = localLibraries
        )

class DynamicLibrary( Library ):
    pass

class StaticLibrary( Library ):
    pass

class StaticLibraryBinary( AtomicArtifact ):
    def __init__( self, buildkit, name, files, objects, localLibraries ):
        AtomicArtifact.__init__(
            self,
            name = name,
            files = files,
            strongDependencies = objects,
            orderOnlyDependencies = [],
            automaticDependencies = []
        )

class LinkedBinary( AtomicArtifact ):
    def __init__( self, buildkit, name, files, objects, localLibraries ):
        self.__librariesToLink, staticLibraryBinaries, dynamicLibraryBinaries = LinkedBinary.__extractLibraries( localLibraries )
        AtomicArtifact.__init__(
            self,
            name = name,
            files = files,
            strongDependencies = objects + staticLibraryBinaries,
            orderOnlyDependencies = dynamicLibraryBinaries,
            automaticDependencies = []
        )

    @staticmethod
    def __extractLibraries( libraries ):
        librariesToLink = []
        staticLibraryBinaries = []
        dynamicLibraryBinaries = []
        for lib in libraries:
            binary = lib.getBinary()
            if binary is None:
                a, b, c = LinkedBinary.__extractLibraries( lib.getLocalLibraries() )
                librariesToLink += a
                staticLibraryBinaries += b
                dynamicLibraryBinaries += c
            else:
                librariesToLink.append( lib )
                if isinstance( binary, DynamicLibraryBinary ):
                    dynamicLibraryBinaries.append( binary )
                elif isinstance( binary, StaticLibraryBinary ):
                    staticLibraryBinaries.append( binary )
                    a, b, c = LinkedBinary.__extractLibraries( lib.getLocalLibraries() )
                    librariesToLink += a
                    staticLibraryBinaries += b
                    dynamicLibraryBinaries += c
        return librariesToLink, staticLibraryBinaries, dynamicLibraryBinaries

    def getLibrariesToLink( self ):
        return self.__librariesToLink

class Executable( LinkedBinary ):
    pass

class DynamicLibraryBinary( LinkedBinary ):
    pass
