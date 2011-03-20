from ViDE.ContextReferer import ContextReferer
from ViDE.Core.Actions import CopyFileAction
from ViDE.Core.Artifact import Artifact, InputArtifact as CoreInputArtifact, AtomicArtifact as CoreAtomicArtifact, CompoundArtifact as CoreCompoundArtifact

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
        return CopyFileAction( self.__source.getFileName(), self.__destination )

    def getDestination( self ):
        return self.__destination

    def getSource( self ):
        return self.__source
