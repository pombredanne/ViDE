import os
import time

import AnotherPyGraphvizAgain.Compounds as gv

from ViDE import Log
from ViDE.Core.Actions import NullAction, CreateDirectoryAction, RemoveFileAction, TouchAction
from ViDE.Core.CallOnceAndCache import CallOnceAndCache

def createAndLabel(cls, label):
    return cls(label.replace(".", "_").replace("/", "_")).set("label", label)

class BuildEmptyArtifact( Exception ):
    pass

class Artifact( CallOnceAndCache ):
    ###################################################################### virtuals to be implemented
    # computeGraphNode
    # computeGraphLinks
    # getAllFiles
    # computeProductionAction
    
    def __init__( self, name, explicit ):
        CallOnceAndCache.__init__( self )
        self.__name = name
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

    def getGraph( self ):
        graph = gv.Graph("artifact")
        graph.set("ranksep", "1")
        graph.nodeAttr.set("shape", "box")
        graph.add( self.getGraphNode() )
        for link in self.getGraphLinks():
            graph.add( link )
        return graph

    def getGraphNode( self ):
        return self.getCached( "graphNode", self.computeGraphNode )

    def getGraphLinks( self ):
        return self.getCached( "graphLinks", self.computeGraphLinks )

    def getProductionAction( self, assumeNew = [], assumeOld = [], touch = False, createDirectoryActions = None ):
        if createDirectoryActions is None:
            createDirectoryActions = dict()
        return self.getCached( "productionAction", lambda n, o, t: self.computeProductionAction( n, o, t, createDirectoryActions ), assumeNew, assumeOld, touch )

    def mustBeProduced( self, assumeNew, assumeOld, touch ):
        return self.getCached( "mustBeProduced", self.computeIfMustBeProduced, assumeNew, assumeOld, touch )

class InputArtifact( Artifact ):
    def __init__( self, name, files, explicit ):
        if len( files ) == 0:
            raise BuildEmptyArtifact( "Trying to build an empty InputArtifact" )
        Artifact.__init__( self, name, explicit )
        self.__files = files

    def computeProductionAction( self, assumeNew, assumeOld, touch, createDirectoryActions ):
        return NullAction()

    def computeIfMustBeProduced( self, assumeNew, assumeOld, touch ):
        return False

    def getAllFiles( self ):
        return self.__files

    def computeGraphNode( self ):
    ### @todo Factorize with AtomicArtifact.computeGraphNode
        if len( self.__files ) == 1 and self.__files[ 0 ] == self.getName():
            node = createAndLabel(gv.Node, self.getName())
        else:
            node = createAndLabel(gv.Cluster, self.getName())
            node.set("style", "solid")
            for f in self.__files:
                node.add(createAndLabel(gv.Node, f))
        if self.explicit:
            node.set("style", "bold")
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

    def computeProductionAction( self, assumeNew, assumeOld, touch, createDirectoryActions ):
        if self.mustBeProduced( assumeNew, assumeOld, touch ):
            if touch:
                productionAction = TouchAction( self.__files )
            else:
                productionAction = self.doGetProductionAction()
            directories = set( os.path.dirname( f ) for f in self.__files )
            for d in directories:
                if not d in createDirectoryActions:
                    createDirectoryActions[ d ] = CreateDirectoryAction( d )
                productionAction.addPredecessor( createDirectoryActions[ d ] )
            if not touch:
                for f in self.__files:
                    productionAction.addPredecessor( RemoveFileAction( f ) )
        else:
            Log.debug( "Do not produce", self.__files )
            productionAction = NullAction()
        for d in self.__strongDependencies + self.__orderOnlyDependencies + self.__automaticDependencies:
            if d.mustBeProduced( assumeNew, assumeOld, touch ):
                predecessorAction = d.getProductionAction( assumeNew, assumeOld, touch, createDirectoryActions )
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
            node = createAndLabel(gv.Node, self.getName())
        else:
            node = createAndLabel(gv.Cluster, self.getName())
            node.set("style", "solid")
            for f in self.__files:
                node.add(createAndLabel(gv.Node, f))
        if self.explicit:
            node.set("style", "bold")
        return node

    def computeGraphLinks( self ):
        links = []
        for d in self.__strongDependencies:
            links.append( gv.Link( self.getGraphNode(), d.getGraphNode() ) )
        for d in self.__automaticDependencies:
            link = gv.Link( self.getGraphNode(), d.getGraphNode() )
            link.set("color", "grey")
            links.append( link )
        for d in self.__orderOnlyDependencies:
            link = gv.Link( self.getGraphNode(), d.getGraphNode() )
            link.set("style", "dashed")
            links.append( link )
        return links

class CompoundArtifact( Artifact ):
    def __init__( self, name, componants, explicit ):
        if len( componants ) == 0:
            raise BuildEmptyArtifact( "Trying to build an empty CompoundArtifact" )
        Artifact.__init__( self, name, explicit )
        self.__componants = componants

    def computeProductionAction( self, assumeNew, assumeOld, touch, createDirectoryActions ):
        productionAction = NullAction()
        for c in self.__componants:
            productionAction.addPredecessor( c.getProductionAction( assumeNew, assumeOld, touch, createDirectoryActions ) )
        return productionAction

    def getAllFiles( self ):
        allFiles = []
        for c in self.__componants:
            allFiles += c.getAllFiles()
        return allFiles

    def computeGraphNode( self ):
        node = createAndLabel(gv.Cluster, self.getName())
        node.set("style", "solid")
        for c in self.__componants:
            node.add( c.getGraphNode() )
        if self.explicit:
            node.set("style", "bold")
        return node

    def computeGraphLinks( self ):
        links = []
        for c in self.__componants:
            links += c.getGraphLinks()
        return links

    def computeIfMustBeProduced( self, assumeNew, assumeOld, touch ):
        return any( c.mustBeProduced( assumeNew, assumeOld, touch ) for c in self.__componants )

class SubatomicArtifact( Artifact ):
    def __init__( self, name, atomicArtifact, files, explicit ):
        Artifact.__init__(
            self,
            name,
            explicit
        )
        self.__atomicArtifact = atomicArtifact
        self.__files = files

    def computeGraphNode( self ):
        ### @todo Factorize with AtomicArtifact.computeGraphNode
        if len( self.__files ) == 1 and self.__files[ 0 ] == self.getName():
            node = createAndLabel(gv.Node, self.getName())
        else:
            node = createAndLabel(gv.Cluster, self.getName())
            node.set("style", "solid")
            for f in self.__files:
                node.add(createAndLabel(gv.Node, f))
        if self.explicit:
            node.set("style", "bold")
        return node

    def computeGraphLinks( self ):
        return [ gv.Link( self.getGraphNode(), self.__atomicArtifact.getGraphNode() ) ]

    def getAllFiles( self ):
        return self.__files

    def computeIfMustBeProduced( self, assumeNew, assumeOld, touch ):
        return self.__atomicArtifact.mustBeProduced( assumeNew, assumeOld, touch )

    def computeProductionAction( self, assumeNew, assumeOld, touch, createDirectoryActions ):
        return self.__atomicArtifact.getProductionAction( assumeNew, assumeOld, touch, createDirectoryActions )
