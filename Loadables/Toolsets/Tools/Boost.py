import os.path

from ViDE.Toolset import Tool, DownloadUnarchiveConfigureMakeMakeinstall

class BoostLibrary:
	def getBoostLibName( self, name ):
		return "boost_" + name + "-mt" # Cygwin-specific

class BoostPython( Tool, BoostLibrary ):
    def getDependencies( self ):
        return []

    def getIncludeDirectories( self, context ):
        return []

    def getLibPath( self ):
        return None

    def getLibName( self ):
        return self.getBoostLibName( "python" )
        
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