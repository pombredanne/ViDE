import os
import time

from Misc import Graphviz

from ViDE.Core.Actions import NullAction, CreateDirectoryAction, RemoveFileAction, TouchAction
from ViDE import Log

class BuildEmptyArtifact( Exception ):
    pass

class Artifact:
    ###################################################################### virtuals to be implemented
    # computeGraphNode
    # computeGraphLinks
    # getAllFiles
    # computeProductionAction
    
    def __init__( self, name, explicit ):
        self.__name = name
        self.__cachedGraphNode = None
        self.__cachedGraphLinks = None
        self.__cachedProductionAction = dict()
        self.__cachedMustBeProduced = dict()
        self.explicit = explicit

    @staticmethod
    def getModificationDate( file, assumeNew, assumeOld ):
        if file in assumeNew:
            return time.time()
        if file in assumeOld:
            return 0
        return os.stat( file ).st_mtime

    def getOldestFile( self, assumeNew, assumeOld ):
        return min( Artifact.getModificationDate( f, assumeNew, assumeOld ) for f in self.getAllFiles() )

    def getNewestFile( self, assumeNew, assumeOld ):
        return max( Artifact.getModificationDate( f, assumeNew, assumeOld ) for f in self.getAllFiles() )
    
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

    def getProductionAction( self, assumeNew = [], assumeOld = [], touch = False ):
        key = ":".join( assumeNew ) + " " + ":".join( assumeOld ) + str( touch )
        if not self.__cachedProductionAction.has_key( key ):
            self.__cachedProductionAction[ key ] = self.computeProductionAction( assumeNew, assumeOld, touch )
        return self.__cachedProductionAction[ key ]

    def mustBeProduced( self, assumeNew, assumeOld, touch ):
        key = ":".join( assumeNew ) + " " + ":".join( assumeOld ) + str( touch )
        if not self.__cachedMustBeProduced.has_key( key ):
            self.__cachedMustBeProduced[ key ] = self.computeIfMustBeProduced( assumeNew, assumeOld, touch )
        return self.__cachedMustBeProduced[ key ]

class InputArtifact( Artifact ):
    def __init__( self, name, files, explicit ):
        if len( files ) == 0:
            raise BuildEmptyArtifact( "Trying to build an empty InputArtifact" )
        Artifact.__init__( self, name, explicit )
        self.__files = files

    def computeProductionAction( self, assumeNew, assumeOld, touch ):
        return NullAction()

    def computeIfMustBeProduced( self, assumeNew, assumeOld, touch ):
        return False

    def getAllFiles( self ):
        return self.__files

    def computeGraphNode( self ):
    ### @todo Factorize with AtomicArtifact.computeGraphNode
        if len( self.__files ) == 1 and self.__files[ 0 ] == self.getName():
            node = Graphviz.Node( self.getName() )
        else:
            node = Graphviz.Cluster( self.getName() )
            node.attr[ "style" ] = "solid"
            for f in self.__files:
                node.add( Graphviz.Node( f ) )
        if self.explicit:
            node.attr[ "style" ] = "bold"
        return node

    def computeGraphLinks( self ):
        return []

class AtomicArtifact( Artifact ):
    def __init__( self, name, files, strongDependencies, orderOnlyDependencies, automaticDependencies, explicit ):
        if len( files ) == 0:
            raise BuildEmptyArtifact( "Trying to build an empty AtomicArtifact" )
        Artifact.__init__( self, name, explicit )
        self.__files = files
        self.__strongDependencies = strongDependencies
        self.__orderOnlyDependencies = orderOnlyDependencies
        self.__automaticDependencies = automaticDependencies

    def computeProductionAction( self, assumeNew, assumeOld, touch ):
        if self.mustBeProduced( assumeNew, assumeOld, touch ):
            if touch:
                productionAction = TouchAction( self.__files )
            else:
                productionAction = self.doGetProductionAction()
            directories = set( os.path.dirname( f ) for f in self.__files )
            for d in directories:
                productionAction.addPredecessor( CreateDirectoryAction( d ) )
            if not touch:
                for f in self.__files:
                    productionAction.addPredecessor( RemoveFileAction( f ) )
        else:
            Log.debug( "Do not produce", self.__files )
            productionAction = NullAction()
        for d in self.__strongDependencies + self.__orderOnlyDependencies + self.__automaticDependencies:
            if d.mustBeProduced( assumeNew, assumeOld, touch ):
                predecessorAction = d.getProductionAction( assumeNew, assumeOld, touch )
                productionAction.addPredecessor( predecessorAction )
        return productionAction

    def computeIfMustBeProduced( self, assumeNew, assumeOld, touch ):
        return (
            self.__anyFileIsMissing()
            or self.__anyStrongDependencyWillBeProduced( assumeNew, assumeOld, touch )
            or self.__anyStrongDependencyIsMoreRecent( assumeNew, assumeOld )
        )

    def __anyFileIsMissing( self ):
        return any( self.__fileIsMissing( f ) for f in self.__files )

    def __fileIsMissing( self, f ):
        if not os.path.exists( f ):
            Log.verbose( "Produce", self.__files, "because", f, "is missing" )
            return True
        return False

    def __anyStrongDependencyWillBeProduced( self, assumeNew, assumeOld, touch ):
        for d in self.__strongDependencies + self.__automaticDependencies:
            if d.mustBeProduced( assumeNew, assumeOld, touch ):
                Log.verbose( "Produce", self.__files, "because", d.getName(), "is produced" )
                return True
        return False

    def __anyStrongDependencyIsMoreRecent( self, assumeNew, assumeOld ):
        selfOldestModificationDate = self.getOldestFile( assumeNew, assumeOld )
        for d in self.__strongDependencies + self.__automaticDependencies:
            depNewestModificationDate = d.getNewestFile( assumeNew, assumeOld )
            if depNewestModificationDate >= selfOldestModificationDate:
                Log.verbose( "Produce", self.__files, "because", d.getName(), "is more recent" )
                return True
        return False

    def getAllFiles( self ):
        return self.__files
        
    def computeGraphNode( self ):
        if len( self.__files ) == 1 and self.__files[ 0 ] == self.getName():
            node = Graphviz.Node( self.getName() )
        else:
            node = Graphviz.Cluster( self.getName() )
            node.attr[ "style" ] = "solid"
            for f in self.__files:
                node.add( Graphviz.Node( f ) )
        if self.explicit:
            node.attr[ "style" ] = "bold"
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
    def __init__( self, name, componants, explicit ):
        if len( componants ) == 0:
            raise BuildEmptyArtifact( "Trying to build an empty CompoundArtifact" )
        Artifact.__init__( self, name, explicit )
        self.__componants = componants

    def computeProductionAction( self, assumeNew, assumeOld, touch ):
        productionAction = NullAction()
        for c in self.__componants:
            productionAction.addPredecessor( c.getProductionAction( assumeNew, assumeOld, touch ) )
        return productionAction

    def getAllFiles( self ):
        allFiles = []
        for c in self.__componants:
            allFiles += c.getAllFiles()
        return allFiles

    def computeGraphNode( self ):
        node = Graphviz.Cluster( self.getName() )
        node.attr[ "style" ] = "solid"
        for c in self.__componants:
            node.add( c.getGraphNode() )
        if self.explicit:
            node.attr[ "style" ] = "bold"
        return node

    def computeGraphLinks( self ):
        links = []
        for c in self.__componants:
            links += c.getGraphLinks()
        return links
        
    def computeIfMustBeProduced( self, assumeNew, assumeOld, touch ):
        return any( c.mustBeProduced( assumeNew, assumeOld, touch ) for c in self.__componants )
