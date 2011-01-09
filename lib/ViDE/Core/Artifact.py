import os

from Misc import Graphviz

from ViDE.Core.Actions import NullAction, CreateDirectoryAction, RemoveFileAction

class Artifact:
    def __init__( self, name, automatic ):
        self.__name = name
        self.__automatic = automatic
        self.__graphNode = None
        self.__graphLinks = None

    @staticmethod
    def getModificationDate( file ):
        return os.stat( file ).st_mtime

    def getOldestFile( self ):
        return min( Artifact.getModificationDate( f ) for f in self.getAllFiles() )

    def getNewestFile( self ):
        return max( Artifact.getModificationDate( f ) for f in self.getAllFiles() )
    
    def getName( self ):
        return self.__name

    def getGraphNode( self ):
        if self.__graphNode is None:
            self.__graphNode = self.computeGraphNode()
        return self.__graphNode

    def getGraphLinks( self ):
        if self.__graphLinks is None:
            self.__graphLinks = self.computeGraphLinks()
        return self.__graphLinks

class InputArtifact( Artifact ):
    def __init__( self, name, files, automatic ):
        Artifact.__init__( self, name, automatic )
        self.__files = files

    def mustBeProduced( self ):
        return False

    def getProductionAction( self ):
        return None
        
    def getAllFiles( self ):
        return self.__files

    def computeGraphNode( self ):
        node = Graphviz.Cluster( self.getName() )
        for f in self.__files:
            node.add( Graphviz.Node( f ) )
        return node

    def computeGraphLinks( self ):
        return []
        
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
                productionAction.addPredecessor( CreateDirectoryAction.getOrCreate( d ) )
            for f in self.__files:
                productionAction.addPredecessor( RemoveFileAction( f ) )
        else:
            productionAction = NullAction()
        for d in self.__strongDependencies + self.__orderOnlyDependencies:
            predecessorAction = d.getProductionAction()
            if predecessorAction is not None:
                productionAction.addPredecessor( predecessorAction )
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
        
    def computeGraphNode( self ):
        node = Graphviz.Cluster( self.getName() )
        for f in self.__files:
            node.add( Graphviz.Node( f ) )
        return node

    def computeGraphLinks( self ):
        links = []
        for d in self.__strongDependencies:
            links.append( Graphviz.Link( self.getGraphNode(), d.getGraphNode() ) )
        for d in self.__orderOnlyDependencies:
            link = Graphviz.Link( self.getGraphNode(), d.getGraphNode() )
            link.attr[ "style" ] = "dashed"
            links.append( link )
        return links

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

    def computeGraphNode( self ):
        node = Graphviz.Cluster( self.getName() )
        for c in self.__componants:
            node.add( c.getGraphNode() )
        return node

    def computeGraphLinks( self ):
        links = []
        for c in self.__componants:
            links += c.getGraphLinks()
        return links
