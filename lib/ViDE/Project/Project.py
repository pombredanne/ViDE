from ViDE.Core.Descriptible import Descriptible
from ViDE.Core.Action import NullAction

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
