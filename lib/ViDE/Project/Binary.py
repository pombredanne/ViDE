import os.path

from ViDE.Core.Actions import CopyFileAction
from ViDE.Core.Artifact import AtomicArtifact, CompoundArtifact

class Binary( AtomicArtifact ):
    def __init__( self, buildkit, name, files, objects, localLibraries ):
        self.__localLibraries = localLibraries
        AtomicArtifact.__init__(
            self,
            name = name,
            files = files,
            strongDependencies = objects,
            orderOnlyDependencies = [ lib.getBinary() for lib in self.localLibrariesWithBinary() ],
            automaticDependencies = []
        )

    def localLibrariesWithBinary( self ):
        libs = []
        for lib in self.__localLibraries:
            if hasattr( lib, "getBinary" ):
                libs.append( lib )
            libs += lib.localLibrariesWithBinaryToTransmit()
        return libs

class Executable( Binary ):
    pass

class StaticLibraryBinary( Binary ):
    pass

class DynamicLibraryBinary( Binary ):
    pass

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

class LibraryWithBinary( CompoundArtifact ):
    @staticmethod
    def computeName( buildkit, name, headers, binary, localLibraries ):
        return "lib" + name

    def __init__( self, buildkit, name, headers, binary, localLibraries ):
        self.__libName = name
        self.__binary = binary
        self.__copiedHeaders = CopiedHeaders( buildkit, name, headers )
        CompoundArtifact.__init__( self, name = "lib" + name, componants = [ self.__binary, self.__copiedHeaders ] )
        
    def getLibName( self ):
        return self.__libName
        
    def getBinary( self ):
        return self.__binary

    def getCopiedHeaders( self ):
        return self.__copiedHeaders

class DynamicLibrary( LibraryWithBinary ):
    def localLibrariesWithBinaryToTransmit( self ):
        return []

class StaticLibrary( LibraryWithBinary ):
    def __init__( self, buildkit, name, headers, binary, localLibraries ):
        self.__localLibraries = localLibraries
        LibraryWithBinary.__init__( self, buildkit, name, headers, binary, localLibraries )

    def localLibrariesWithBinaryToTransmit( self ):
        libs = []
        for lib in self.__localLibraries:
            if hasattr( lib, "getBinary" ):
                libs.append( lib )
            libs += lib.localLibrariesWithBinaryToTransmit()
        return libs

class HeaderLibrary( CompoundArtifact ):
    @staticmethod
    def computeName( buildkit, name, headers, localLibraries ):
        return "lib" + name

    def __init__( self, buildkit, name, headers, localLibraries ):
        self.__libName = name
        self.__copiedHeaders = CopiedHeaders( buildkit, name, headers )
        self.__localLibraries = localLibraries
        CompoundArtifact.__init__( self, name = "lib" + name, componants = [ self.__copiedHeaders ] )

    def getLibName( self ):
        return self.__libName

    def getCopiedHeaders( self ):
        return self.__copiedHeaders

    def localLibrariesWithBinaryToTransmit( self ):
        libs = []
        for lib in self.__localLibraries:
            if hasattr( lib, "getBinary" ):
                libs.append( lib )
            libs += lib.localLibrariesWithBinaryToTransmit()
        return libs
