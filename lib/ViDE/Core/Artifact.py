import os

from Action import Action, NullAction

class RemoveFileAction( Action ):
    def __init__( self, file ):
        Action.__init__( self )
        self.__file = file

    def doPreview( self ):
        return "rm -f " + self.__file
        
    def doExecute( self ):
        print "rm -f " + self.__file
        try:
            os.unlink( self.__file )
        except OSError:
            pass

class CreateDirectoryAction( Action ):
    def __init__( self, directory ):
        Action.__init__( self )
        self.__directory = directory

    def doPreview( self ):
        return "mkdir -p " + self.__directory
        
    def doExecute( self ):
        print "mkdir -p " + self.__directory
        try:
            os.makedirs( self.__directory )
        except OSError:
            pass
        
class Artifact:
    def __init__( self, name, automatic ):
        self.__name = name
        self.__automatic = automatic

    @staticmethod
    def getModificationDate( file ):
        return os.stat( file ).st_mtime

    def getOldestFile( self ):
        return min( Artifact.getModificationDate( f ) for f in self.getAllFiles() )

    def getNewestFile( self ):
        return max( Artifact.getModificationDate( f ) for f in self.getAllFiles() )

class InputArtifact( Artifact ):
    def __init__( self, name, files, automatic ):
        Artifact.__init__( self, name, automatic )
        self.__files = files

    def mustBeProduced( self ):
        return False

    def getProductionAction( self ):
        return NullAction()
        
    def getAllFiles( self ):
        return self.__files

class ProduceableArtifact( Artifact ):
    def __init__( self, name, automatic ):
        Artifact.__init__( self, name, automatic )
        self.__productionAction = None

    def getProductionAction( self ):
        if self.__productionAction is None:
            if self.mustBeProduced():
                self.__productionAction = self.computeProductionAction()
            else:
                self.__productionAction = NullAction()
        return self.__productionAction

class AtomicArtifact( ProduceableArtifact ):
    def __init__( self, name, files, strongDependencies, orderOnlyDependencies, automatic ):
        if len( files ) == 0:
            raise Exception( "Trying to build an empty AtomicArtifact" )
        ProduceableArtifact.__init__( self, name, automatic )
        self.__files = files
        self.__strongDependencies = strongDependencies
        self.__orderOnlyDependencies = orderOnlyDependencies

    def computeProductionAction( self ):
        if self.__filesMustBeProduced():
            productionAction = self.doGetProductionAction()
            directories = set( os.path.dirname( f ) for f in self.__files )
            for d in directories:
                productionAction.addPredecessor( CreateDirectoryAction( d ) )
            for f in self.__files:
                productionAction.addPredecessor( RemoveFileAction( f ) )
        else:
            productionAction = NullAction()
        for d in self.__strongDependencies + self.__orderOnlyDependencies:
            productionAction.addPredecessor( d.getProductionAction() )
        return productionAction

    def mustBeProduced( self ):
        return self.__filesMustBeProduced() or self.__anyOrderOnlyDependencyMustBeProduced()
        
    def __filesMustBeProduced( self ):
        return (
            self.__anyFileIsMissing()
            or self.__anyStrongDependencyMustBeProduced()
            or self.__anyStrongDependencyIsMoreRecent()
        )

    def __anyFileIsMissing( self ):
        return any( AtomicArtifact.__fileIsMissing( f ) for f in self.__files )

    @staticmethod
    def __fileIsMissing( f ):
        return not os.path.exists( f )

    def __anyStrongDependencyMustBeProduced( self ):
        return any( d.mustBeProduced() for d in self.__strongDependencies )

    def __anyOrderOnlyDependencyMustBeProduced( self ):
        return any( d.mustBeProduced() for d in self.__orderOnlyDependencies )

    def __anyStrongDependencyIsMoreRecent( self ):
        selfOldestModificationDate = self.getOldestFile()
        for d in self.__strongDependencies:
            depNewestModificationDate = d.getNewestFile()
            if depNewestModificationDate >= selfOldestModificationDate:
                return True
        return False

    def getAllFiles( self ):
        return self.__files

class CompoundArtifact( ProduceableArtifact ):
    def __init__( self, name, componants, automatic ):
        if len( componants ) == 0:
            raise Exception( "Trying to build an empty CompoundArtifact" )
        ProduceableArtifact.__init__( self, name, automatic )
        self.__componants = componants

    def computeProductionAction( self ):
        productionAction = NullAction()
        for c in self.__componants:
            productionAction.addPredecessor( c.getProductionAction() )
        return productionAction

    def mustBeProduced( self ):
        return True

    def getAllFiles( self ):
        allFiles = []
        for c in self.__componants:
            allFiles += c.getAllFiles()
        return allFiles
