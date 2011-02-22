from ViDE.Project.Description import *
from ViDE.Core.Artifact import AtomicArtifact, SubatomicArtifact

class XsdSchema( MonofileInputArtifact ):
    pass

class GeneratedSource( AtomicArtifact ):
    def computeName( buildkit, xsdSchema, explicit ):
        return xsdSchema.getFileName() + "_tree"

    def __init__( self, buildkit, xsdSchema, explicit ):
        AtomicArtifact.__init__(
            self,
            name = xsdSchema.getFileName() + "_tree",
            files = [ buildkit.fileName( "gen", xsdSchema.getFileName() + ".hpp" ), buildkit.fileName( "gen", xsdSchema.getFileName() + ".cpp" ) ],
            strongDependencies = [ xsdSchema ],
            orderOnlyDependencies = [],
            automaticDependencies = [],
            explicit = explicit
        )
        
    def getSource( self ):
        return self.getCached( "cpp", lambda: Project.inProgress.createOrRetrieve( XsdSchema, schema, False )

def Xsd( schema ):
    schema = Project.inProgress.createOrRetrieve( XsdSchema, schema, False )
    return Project.inProgress.createOrRetrieve( GeneratedSource, schema, True )

a = Xsd( "a.xsd" )

CppExecutable(
    name = "hello",
    # sources = [ "main.cpp", a.getSource() ]
    sources = [ "main.cpp" ]
)
