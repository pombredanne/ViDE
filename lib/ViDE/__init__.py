import os.path

def rootDirectory():
    return os.path.relpath( os.path.dirname( os.path.dirname( os.path.dirname( os.path.realpath( __file__ ) ) ) ) )

def libDirectory():
    return os.path.join( rootDirectory(), "lib" )

def buildkitsDirectory():
    return os.path.join( rootDirectory(), "Buildkits" )

def toolsetsDirectory():
    return os.path.join( rootDirectory(), "Toolsets" )
def toolsetsTmpDirectory():
    return os.path.join( toolsetsDirectory(), "Build" )
def toolsetsInstallDirectory():
    return os.path.join( toolsetsDirectory(), "Install" )
def toolsetsMarkerDirectory():
    return os.path.join( toolsetsDirectory(), "Marker" )

def toolsDirectory():
    return os.path.join( toolsetsDirectory(), "Tools" )
def toolsCacheDirectory():
    return os.path.join( toolsDirectory(), "Cache" )
