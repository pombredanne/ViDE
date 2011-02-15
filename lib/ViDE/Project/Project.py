import os

from Misc import Graphviz

from ViDE.Core.Descriptible import Descriptible
from ViDE.Core.Actions import NullAction

class Project( Descriptible ):
    @classmethod
    def load( cls, buildkit, projectDirectory = "." ):
        return Project.loadFromDescription( os.path.join( projectDirectory, "videfile.py" ), buildkit )

    def __init__( self, buildkit ):
        Descriptible.__init__( self )
        self.buildkit = buildkit
        self.__artifacts = []

    def createOrRetrieve( self, artifactClass, *args ):
        if hasattr( artifactClass, "needsBuildkit" ):
            name = artifactClass.computeName( self.buildkit, *args )
        else:
            name = artifactClass.computeName( *args )
        for artifact in self.__artifacts:
            if artifact.getName() == name:
                return artifact
        if hasattr( artifactClass, "needsBuildkit" ):
            artifact = artifactClass( self.buildkit, *args )
        else:
            artifact = artifactClass( *args )
        self.__addArtifact( artifact )
        return artifact
        
    def __addArtifact( self, artifact ):
        self.__artifacts.append( artifact )
        
    def getBuildAction( self ):
        action = NullAction()
        for artifact in self.__artifacts:
            action.addPredecessor( artifact.getProductionAction() )
        return action.prune()

    def getGraph( self ):
        graph = Graphviz.Graph( "Project" )
        graph.attr[ "ranksep" ] = "1"
        graph.nodeAttr[ "shape" ] = "box"
        for artifact in self.__artifacts:
            graph.add( artifact.getGraphNode() )
            for link in artifact.getGraphLinks():
                graph.add( link )
        return graph
