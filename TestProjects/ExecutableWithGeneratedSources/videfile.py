import ActionTree.StockActions as actions

from ViDE.Project.Description import *
from ViDE.Project.Artifacts.BasicArtifacts import AtomicArtifact, SubatomicArtifact, MonofileInputArtifact

class XsdSchema( MonofileInputArtifact ):
    pass

class XsdGeneratedSource( SubatomicArtifact ):
    def __init__( self, context, fileName, atomicArtifact, explicit ):
        SubatomicArtifact.__init__(
            self,
            context = context,
            name = fileName,
            atomicArtifact = atomicArtifact,
            files = [ fileName ],
            explicit = explicit
        )
        self.__fileName = fileName

    def getFileName( self ):
        return self.__fileName

class GeneratedSource( AtomicArtifact ):
    def __init__( self, context, xsdSchema, explicit ):
        self.__hppFileName = context.fileName( "gen", xsdSchema.getFileName() + ".hpp" )
        self.__cppFileName = context.fileName( "gen", xsdSchema.getFileName() + ".cpp" )
        AtomicArtifact.__init__(
            self,
            context = context,
            name = xsdSchema.getFileName() + "_tree",
            files = [ self.__hppFileName, self.__cppFileName ],
            strongDependencies = [ xsdSchema ],
            orderOnlyDependencies = [],
            automaticDependencies = [],
            explicit = explicit
        )

    def getSource( self ):
        return self.getCached( "cpp", lambda: Project.inProgress.createArtifact( XsdGeneratedSource, self.__cppFileName, self, False ) )

    def doGetProductionAction( self ):
        a = actions.Sleep(1)
        a.addDependency(actions.TouchFile(self.__hppFileName))
        a.addDependency(actions.TouchFile(self.__cppFileName))
        return a

def Xsd( schema ):
    schema = Project.inProgress.createArtifact( XsdSchema, schema, False )
    return Project.inProgress.createArtifact( GeneratedSource, schema, True )

a = Xsd( "a.xsd" )

CppExecutable(
    name = "hello",
    sources = [ "main.cpp", a.getSource() ]
)
