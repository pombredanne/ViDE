from Misc import Graphviz

from ViDE.Core.Descriptible import Descriptible
from ViDE.Core.Actions import NullAction

class Project( Descriptible ):
    def beginDescription( self ):
        self.__artifacts = []
        
    def addArtifact( self, artifact ):
        self.__artifacts.append( artifact )

    def endDescription( self ):
        pass

    def getBuildAction( self ):
        action = NullAction()
        for artifact in self.__artifacts:
            action.addPredecessor( artifact.getProductionAction() )
        return action

    def getGraph( self ):
        graph = Graphviz.Graph( "Project" )
        graph.attr[ "ranksep" ] = "1"
        for artifact in self.__artifacts:
            graph.add( artifact.getGraphNode() )
            for link in artifact.getGraphLinks():
                graph.add( link )
        return graph
        