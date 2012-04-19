import os.path

import ViDE
from ViDE.Toolset import Tool, DownloadUnarchiveConfigureMakeMakeinstall

class BoostLibrary:
	def getBoostLibName( self, name ):
		return "boost_" + name + "-mt" # Cygwin-and-Linux-specific

class BoostPython( Tool, BoostLibrary ):
    def getDependencies( self ):
        return []

    def getIncludeDirectories( self, context ):
        return []

    def getLibPath( self ):
        return None

    def getLibName( self ):
        return self.getBoostLibName( "python" ) + ( "-py27" if ViDE.host() == "linux" else "" )
        
class BoostUnitTestFramework( Tool, BoostLibrary ):
    def getDependencies( self ):
        return []

    def getIncludeDirectories( self, context ):
        return []

    def getLibPath( self ):
        return None

    def getLibName( self ):
        return self.getBoostLibName( "unit_test_framework" )
        
class BoostProgramOptions( Tool, BoostLibrary ):
    def getDependencies( self ):
        return []

    def getIncludeDirectories( self, context ):
        return []

    def getLibPath( self ):
        return None

    def getLibName( self ):
        return self.getBoostLibName( "program_options" )
        
class BoostThread( Tool, BoostLibrary ):
    def getDependencies( self ):
        return []

    def getIncludeDirectories( self, context ):
        return []

    def getLibPath( self ):
        return None

    def getLibName( self ):
        return self.getBoostLibName( "thread" )
        
class BoostDateTime( Tool, BoostLibrary ):
    def getDependencies( self ):
        return []

    def getIncludeDirectories( self, context ):
        return []

    def getLibPath( self ):
        return None

    def getLibName( self ):
        return self.getBoostLibName( "date_time" )
