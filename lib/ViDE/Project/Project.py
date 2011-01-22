from Misc import Graphviz

from ViDE.Core.Descriptible import Descriptible
from ViDE.Core.Actions import NullAction

class Project( Descriptible ):
    def __init__( self, buildKit ):
        Descriptible.__init__( self )
        self.__buildKit = buildKit
        self.__artifacts = []
        
    def addArtifact( self, artifact ):
        self.__artifacts.append( artifact )
        
    def createOrRetrieve( self, artifactClass, *args ):
        name = artifactClass.computeName( *args )
        for artifact in self.__artifacts:
            if artifact.getName() == name:
                return artifact
        artifact = artifactClass( *args )
        self.addArtifact( artifact )
        return artifact

    def getBuildAction( self ):
        action = NullAction()
        for artifact in self.__artifacts:
            action.addPredecessor( artifact.getProductionAction() )
        return action

    def getGraph( self ):
        graph = Graphviz.Graph( "Project" )
        graph.attr[ "ranksep" ] = "1"
        graph.nodeAttr[ "shape" ] = "box"
        for artifact in self.__artifacts:
            graph.add( artifact.getGraphNode() )
            for link in artifact.getGraphLinks():
                graph.add( link )
        return graph
