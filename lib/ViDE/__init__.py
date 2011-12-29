import sys
import os.path

def host():
    if sys.platform == "linux2":
        return "linux"
    elif sys.platform == "cygwin":
        return "cygwin"
    elif sys.platform == "darwin":
        return "darwin"
    elif sys.platform == "win32":
        return "win32"
    else:
        raise Exception( "Unsupported host " + sys.platform )

def rootDirectory():
    return os.path.relpath( os.path.dirname( os.path.dirname( os.path.dirname( os.path.realpath( __file__ ) ) ) ) )

def libDirectory():
    return os.path.join( rootDirectory(), "lib" )

def toolsetsDirectory():
    return os.path.join( rootDirectory(), "Loadables", "Toolsets" )
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
