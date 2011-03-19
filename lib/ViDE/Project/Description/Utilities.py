from ViDE.Core.Artifact import Artifact

def identity( x ):
    return x

def isArtifact( object ):
    return isinstance( object, Artifact )
