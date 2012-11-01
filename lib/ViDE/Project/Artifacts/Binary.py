from ViDE.Core import SubprocessFoo as Subprocess
from ViDE.Project.Artifacts.BasicArtifacts import CopiedArtifact, AtomicArtifact, CompoundArtifact

class CopiedHeader( CopiedArtifact ):
    def __init__( self, context, header, stripHeaders, explicit ):
        fileName = context.fileName( "inc", stripHeaders( header.getFileName() ) )
        CopiedArtifact.__init__(
            self,
            context = context,
            name = fileName,
            source = header,
            destination = fileName,
            explicit = explicit
        )

class CopiedHeaders( CompoundArtifact ):
    def __init__( self, context, name, headers, stripHeaders, explicit ):
        self.__copiedHeaders = [ CopiedHeader( context, header, stripHeaders, False ) for header in headers ]
        CompoundArtifact.__init__(
            self,
            context = context,
            name = name + "_hdr",
            componants = self.__copiedHeaders,
            explicit = explicit
        )

    def get( self ):
        return self.__copiedHeaders

class Library( CompoundArtifact ):
    def __init__( self, context, name, headers, binary, localLibraries, externalLibraries, stripHeaders, explicit ):
        self.__libName = name
        self.__copiedHeaders = CopiedHeaders( context, name, headers, stripHeaders, False )
        self.__binary = binary
        self.__localLibraries = localLibraries
        componants = [ self.__copiedHeaders ]
        if binary is not None:
            componants.append( binary )
        CompoundArtifact.__init__(
            self,
            context = context,
            name = "lib" + name,
            componants = componants,
            explicit = explicit
        )

    def getLibName( self ):
        return self.__libName

    def getLibPath( self ):
        return None

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
    def __init__( self, context, name, headers, localLibraries, externalLibraries, stripHeaders, explicit ):
        Library.__init__(
            self,
            context = context,
            name = name,
            headers = headers,
            binary = None,
            localLibraries = localLibraries,
            externalLibraries = externalLibraries,
            stripHeaders = stripHeaders,
            explicit = explicit
        )

class DynamicLibrary( Library ):
    pass

class StaticLibrary( Library ):
    pass

class StaticLibraryBinary( AtomicArtifact ):
    def __init__( self, context, name, files, objects, localLibraries, externalLibraries, explicit ):
        AtomicArtifact.__init__(
            self,
            context = context,
            name = name,
            files = files,
            strongDependencies = objects,
            orderOnlyDependencies = [],
            automaticDependencies = [],
            explicit = explicit
        )

class LinkedBinary( AtomicArtifact ):
    def __init__( self, context, name, files, objects, localLibraries, externalLibraries, explicit ):
        self.__librariesToLink, staticLibraryBinaries, dynamicLibraryBinaries = LinkedBinary.__extractLibraries( localLibraries )
        for o in objects:
            self.__librariesToLink += o.getLibrariesToLink()
        AtomicArtifact.__init__(
            self,
            context = context,
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
    def __init__( self, context, name, files, objects, localLibraries, externalLibraries, explicit ):
        LinkedBinary.__init__( self, context, name, files, objects, localLibraries, externalLibraries, explicit )
        self.__executableFile = files[ 0 ]

    def run( self, arguments ):
        Subprocess.execute( [ self.__executableFile ] + arguments, context = self.context )

    def getFileName( self ):
        return self.__executableFile

class DynamicLibraryBinary( LinkedBinary ):
    pass
