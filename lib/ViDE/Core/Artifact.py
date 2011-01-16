import os

from Misc import Graphviz

from ViDE.Core.Actions import NullAction, CreateDirectoryAction, RemoveFileAction

class Artifact:
    ###################################################################### virtuals to be implemented
    # computeGraphNode
    # computeGraphLinks
    # getAllFiles
    # computeProductionAction
    
    def __init__( self, name ):
        self.__name = name
        self.__cachedGraphNode = None
        self.__cachedGraphLinks = None
        self.__cachedProductionAction = None

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
        if self.__cachedGraphNode is None:
            self.__cachedGraphNode = self.computeGraphNode()
        return self.__cachedGraphNode

    def getGraphLinks( self ):
        if self.__cachedGraphLinks is None:
            self.__cachedGraphLinks = self.computeGraphLinks()
        return self.__cachedGraphLinks

    def getProductionAction( self ):
        if self.__cachedProductionAction is None:
            self.__cachedProductionAction = self.computeProductionAction()
        return self.__cachedProductionAction

class InputArtifact( Artifact ):
    def __init__( self, name, files ):
        if len( files ) == 0:
            raise Exception( "Trying to build an empty InputArtifact" )
        Artifact.__init__( self, name )
        self.__files = files

    def computeProductionAction( self ):
        return NullAction()

    def getAllFiles( self ):
        return self.__files

    def computeGraphNode( self ):
        node = Graphviz.Cluster( self.getName() )
        for f in self.__files:
            node.add( Graphviz.Node( f ) )
        return node

    def computeGraphLinks( self ):
        return []

class MonofileInputArtifact( InputArtifact ):
    @staticmethod
    def computeName( fileName ):
        return fileName

    def __init__( self, fileName ):
        if fileName is None or len( fileName ) == 0:
            raise Exception( "Trying to build an empty MonofileInputArtifact" )
        InputArtifact.__init__( self, name = fileName, files = [ fileName ] )
        self.__fileName = fileName
        
    def getFileName( self ):
        return self.__fileName

class AtomicArtifact( Artifact ):
    def __init__( self, name, files, strongDependencies, orderOnlyDependencies, automaticDependencies ):
        if len( files ) == 0:
            raise Exception( "Trying to build an empty AtomicArtifact" )
        Artifact.__init__( self, name )
        self.__files = files
        self.__strongDependencies = strongDependencies
        self.__orderOnlyDependencies = orderOnlyDependencies
        self.__automaticDependencies = automaticDependencies

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
        for d in self.__strongDependencies + self.__orderOnlyDependencies + self.__automaticDependencies:
            predecessorAction = d.getProductionAction()
            productionAction.addPredecessor( predecessorAction )
        return productionAction

    def __filesMustBeProduced( self ):
        return (
            self.__anyFileIsMissing()
            or self.__anyStrongDependencyWillBeProduced()
            or self.__anyStrongDependencyIsMoreRecent()
        )

    def __anyFileIsMissing( self ):
        return any( AtomicArtifact.__fileIsMissing( f ) for f in self.__files )

    @staticmethod
    def __fileIsMissing( f ):
        return not os.path.exists( f )

    def __anyStrongDependencyWillBeProduced( self ):
        return not all( d.getProductionAction().isFullyNull() for d in self.__strongDependencies + self.__automaticDependencies )

    def __anyStrongDependencyIsMoreRecent( self ):
        selfOldestModificationDate = self.getOldestFile()
        for d in self.__strongDependencies + self.__automaticDependencies:
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
        for d in self.__automaticDependencies:
            link = Graphviz.Link( self.getGraphNode(), d.getGraphNode() )
            link.attr[ "color" ] = "grey"
            links.append( link )
        for d in self.__orderOnlyDependencies:
            link = Graphviz.Link( self.getGraphNode(), d.getGraphNode() )
            link.attr[ "style" ] = "dashed"
            links.append( link )
        return links

class CompoundArtifact( Artifact ):
    def __init__( self, name, componants ):
        if len( componants ) == 0:
            raise Exception( "Trying to build an empty CompoundArtifact" )
        Artifact.__init__( self, name )
        self.__componants = componants

    def computeProductionAction( self ):
        productionAction = NullAction()
        for c in self.__componants:
            productionAction.addPredecessor( c.getProductionAction() )
        return productionAction

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
