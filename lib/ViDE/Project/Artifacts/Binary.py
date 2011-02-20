import os.path

from ViDE.Core.Actions import CopyFileAction
from ViDE.Core.Artifact import AtomicArtifact, CompoundArtifact
from ViDE.Project.Artifacts.BasicArtifacts import CopiedArtifact

class CopiedHeader( CopiedArtifact ):
    @staticmethod
    def computeName( buildkit, header, stripHeaders, explicit ):
        return buildkit.fileName( "inc", stripHeaders( header.getFileName() ) )

    def __init__( self, buildkit, header, stripHeaders, explicit ):
        fileName = buildkit.fileName( "inc", stripHeaders( header.getFileName() ) )
        CopiedArtifact.__init__(
            self,
            buildkit,
            name = fileName,
            source = header,
            destination = fileName,
            explicit = explicit
        )

class CopiedHeaders( CompoundArtifact ):
    def __init__( self, buildkit, name, headers, stripHeaders, explicit ):
        self.__copiedHeaders = [ CopiedHeader( buildkit, header, stripHeaders, False ) for header in headers ]
        CompoundArtifact.__init__( self, name = name + "_hdr", componants = self.__copiedHeaders, explicit = explicit )

    def get( self ):
        return self.__copiedHeaders

class Library( CompoundArtifact ):
    @staticmethod
    def computeName( buildkit, name, headers, binary, localLibraries, stripHeaders, explicit ):
        return "lib" + name

    def __init__( self, buildkit, name, headers, binary, localLibraries, stripHeaders, explicit ):
        self.__libName = name
        self.__copiedHeaders = CopiedHeaders( buildkit, name, headers, stripHeaders, False )
        self.__binary = binary
        self.__localLibraries = localLibraries
        componants = [ self.__copiedHeaders ]
        if binary is not None:
            componants.append( binary )
        CompoundArtifact.__init__(
            self,
            name = "lib" + name,
            componants = componants,
            explicit = explicit
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
    def computeName( buildkit, name, headers, localLibraries, stripHeaders, explicit ):
        return Library.computeName( buildkit, name, headers, None, localLibraries, stripHeaders, explicit )

    def __init__( self, buildkit, name, headers, localLibraries, stripHeaders, explicit ):
        Library.__init__(
            self,
            buildkit = buildkit,
            name = name,
            headers = headers,
            binary = None,
            localLibraries = localLibraries,
            stripHeaders = stripHeaders,
            explicit = explicit
        )

class DynamicLibrary( Library ):
    pass

class StaticLibrary( Library ):
    pass

class StaticLibraryBinary( AtomicArtifact ):
    def __init__( self, buildkit, name, files, objects, localLibraries, explicit ):
        AtomicArtifact.__init__(
            self,
            name = name,
            files = files,
            strongDependencies = objects,
            orderOnlyDependencies = [],
            automaticDependencies = [],
            explicit = explicit
        )

class LinkedBinary( AtomicArtifact ):
    def __init__( self, buildkit, name, files, objects, localLibraries, explicit ):
        self.__librariesToLink, staticLibraryBinaries, dynamicLibraryBinaries = LinkedBinary.__extractLibraries( localLibraries )
        AtomicArtifact.__init__(
            self,
            name = name,
            files = files,
            strongDependencies = objects + staticLibraryBinaries,
            orderOnlyDependencies = dynamicLibraryBinaries,
            automaticDependencies = [],
            explicit = explicit
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
