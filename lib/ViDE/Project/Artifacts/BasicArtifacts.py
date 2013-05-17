import ActionTree.StockActions as actions

from ViDE.ContextReferer import ContextReferer
from ViDE.Core.Artifact import Artifact
from ViDE.Core.Artifact import InputArtifact as CoreInputArtifact
from ViDE.Core.Artifact import AtomicArtifact as CoreAtomicArtifact
from ViDE.Core.Artifact import CompoundArtifact as CoreCompoundArtifact
from ViDE.Core.Artifact import SubatomicArtifact as CoreSubatomicArtifact

class InputArtifact( CoreInputArtifact, ContextReferer ):
    def __init__( self, context, name, files, explicit ):
        ContextReferer.__init__( self, context )
        CoreInputArtifact.__init__( self, name, files, explicit )

class AtomicArtifact( CoreAtomicArtifact, ContextReferer ):
    def __init__( self, context, name, files, strongDependencies, orderOnlyDependencies, automaticDependencies, explicit ):
        ContextReferer.__init__( self, context )
        CoreAtomicArtifact.__init__( self, name, files, strongDependencies, orderOnlyDependencies, automaticDependencies, explicit )

class CompoundArtifact( CoreCompoundArtifact, ContextReferer ):
    def __init__( self, context, name, componants, explicit ):
        ContextReferer.__init__( self, context )
        CoreCompoundArtifact.__init__( self, name, componants, explicit )

class SubatomicArtifact( CoreSubatomicArtifact, ContextReferer ):
    def __init__( self, context, name, atomicArtifact, files, explicit ):
        ContextReferer.__init__( self, context )
        CoreSubatomicArtifact.__init__( self, name, atomicArtifact, files, explicit )

class MonofileInputArtifact( InputArtifact ):
    def __init__( self, context, fileName, explicit ):
        InputArtifact.__init__(
            self,
            context = context,
            name = fileName,
            files = [ fileName ],
            explicit = explicit
        )
        self.__fileName = fileName

    def getFileName( self ):
        return self.__fileName

class CopiedArtifact( AtomicArtifact ):
    def __init__( self, context, name, source, destination, explicit ):
        self.__source = source
        self.__destination = name
        AtomicArtifact.__init__(
            self,
            context = context,
            name = destination,
            files = [ destination ],
            strongDependencies = [ source ],
            orderOnlyDependencies = [],
            automaticDependencies = [],
            explicit = explicit
        )

    def doGetProductionAction( self ):
        return actions.CopyFile(self.__source.getFileName(), self.__destination)

    def getDestination( self ):
        return self.__destination

    def getSource( self ):
        return self.__source
