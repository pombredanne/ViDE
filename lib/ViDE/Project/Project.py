import os
import imp

from Misc import Graphviz

from ViDE.Core.Artifact import Artifact, CompoundArtifact
from ViDE.Core.Actions import NullAction

class Project:
    @classmethod
    def load( cls, buildkit, toolset, projectDirectory = "." ):
        descriptionFile = os.path.join( projectDirectory, "videfile.py" )

        instance = Project( buildkit, toolset )

        Project.inProgress = instance
        imp.load_source( "description", descriptionFile )
        del Project.inProgress

        return instance

    def __init__( self, buildkit, toolset ):
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

    def __getArtifact( self, filter = lambda artifact: True ):
        return CompoundArtifact(
            name = "Project",
            componants = [ artifact for artifact in self.__artifacts if filter( artifact ) ],
            explicit = False
        )

    def getBuildAction( self, assumeNew, assumeOld, touch ):
        createDirectoryActions = dict()
        return self.__getArtifact( filter = lambda artifact: artifact.explicit ).getProductionAction( assumeNew = assumeNew, assumeOld = assumeOld, touch = touch, createDirectoryActions = createDirectoryActions )

    def getGraph( self ):
        return self.__getArtifact().getGraph()
