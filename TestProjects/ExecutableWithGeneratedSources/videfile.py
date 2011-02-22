from ViDE.Core.Artifact import AtomicArtifact, SubatomicArtifact
from ViDE.Core.Actions import TouchAction
from ViDE.Project.Description import *
from ViDE.Project.Artifacts.BasicArtifacts import MonofileInputArtifact

class XsdSchema( MonofileInputArtifact ):
    pass

class XsdGeneratedSource( SubatomicArtifact ):
    @staticmethod
    def computeName( buildkit, fileName, atomicArtifact, explicit ):
        return fileName

    def __init__( self, buildkit, fileName, atomicArtifact, explicit ):
        SubatomicArtifact.__init__(
            self,
            name = fileName,
            atomicArtifact = atomicArtifact,
            files = [ fileName ],
            explicit = explicit
        )
        self.__fileName = fileName

    def getFileName( self ):
        return self.__fileName

class GeneratedSource( AtomicArtifact ):
    @staticmethod
    def computeName( buildkit, xsdSchema, explicit ):
        return xsdSchema.getFileName() + "_tree"

    def __init__( self, buildkit, xsdSchema, explicit ):
        self.__hppFileName = buildkit.fileName( "gen", xsdSchema.getFileName() + ".hpp" )
        self.__cppFileName = buildkit.fileName( "gen", xsdSchema.getFileName() + ".cpp" )
        AtomicArtifact.__init__(
            self,
            name = xsdSchema.getFileName() + "_tree",
            files = [ self.__hppFileName, self.__cppFileName ],
            strongDependencies = [ xsdSchema ],
            orderOnlyDependencies = [],
            automaticDependencies = [],
            explicit = explicit
        )
        
    def getSource( self ):
        return self.getCached( "cpp", lambda: Project.inProgress.createOrRetrieve( XsdGeneratedSource, self.__cppFileName, self, False ) )

    def doGetProductionAction( self ):
        return TouchAction( [ self.__hppFileName, self.__cppFileName ] )

def Xsd( schema ):
    schema = Project.inProgress.createOrRetrieve( XsdSchema, schema, False )
    return Project.inProgress.createOrRetrieve( GeneratedSource, schema, True )

a = Xsd( "a.xsd" )

CppExecutable(
    name = "hello",
    sources = [ "main.cpp", a.getSource() ]
)
