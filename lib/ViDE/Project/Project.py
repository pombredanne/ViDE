import os

from Misc import Graphviz

from ViDE.Core.Descriptible import Descriptible
from ViDE.Core.Artifact import Artifact
from ViDE.Core.Actions import NullAction

class Project( Descriptible ):
    @classmethod
    def load( cls, buildkit, projectDirectory = "." ):
        return Project.loadFromDescription( os.path.join( projectDirectory, "videfile.py" ), buildkit )

    def __init__( self, buildkit ):
        Descriptible.__init__( self )
        self.buildkit = buildkit
        self.__artifacts = []

    def createArtifact( self, artifactClass, *args ):
        artifact = artifactClass( self.buildkit, *args )
        self.__addArtifact( artifact )
        return artifact

    def retrieveByName( self, name, cls = Artifact ):
        for artifact in self.__artifacts:
            if isinstance( artifact, cls ) and artifact.getName() == name:
                return artifact

    def retrieveByFile( self, file, cls = Artifact ):
        for artifact in self.__artifacts:
            if isinstance( artifact, cls ) and file in artifact.getAllFiles():
                return artifact

    def __addArtifact( self, artifact ):
        self.__artifacts.append( artifact )
        
    def getBuildAction( self, assumeNew, assumeOld, touch ):
        action = NullAction()
        for artifact in self.__artifacts:
            action.addPredecessor( artifact.getProductionAction( assumeNew = assumeNew, assumeOld = assumeOld, touch = touch ) )
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
