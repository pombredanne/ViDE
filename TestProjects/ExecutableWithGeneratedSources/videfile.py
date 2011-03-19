from ViDE.Core.Artifact import AtomicArtifact, SubatomicArtifact
from ViDE.Core.Actions import TouchAction
from ViDE.Project.Description import *
from ViDE.Project.Artifacts.BasicArtifacts import MonofileInputArtifact

class XsdSchema( MonofileInputArtifact ):
    pass

class XsdGeneratedSource( SubatomicArtifact ):
    def __init__( self, context, fileName, atomicArtifact, explicit ):
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
    def __init__( self, context, xsdSchema, explicit ):
        self.__hppFileName = context.bk.fileName( "gen", xsdSchema.getFileName() + ".hpp" )
        self.__cppFileName = context.bk.fileName( "gen", xsdSchema.getFileName() + ".cpp" )
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
        return self.getCached( "cpp", lambda: Project.inProgress.createArtifact( XsdGeneratedSource, self.__cppFileName, self, False ) )

    def doGetProductionAction( self ):
        return TouchAction( [ self.__hppFileName, self.__cppFileName ] )

def Xsd( schema ):
    schema = Project.inProgress.createArtifact( XsdSchema, schema, False )
    return Project.inProgress.createArtifact( GeneratedSource, schema, True )

a = Xsd( "a.xsd" )

CppExecutable(
    name = "hello",
    sources = [ "main.cpp", a.getSource() ]
)
