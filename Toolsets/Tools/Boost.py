import os.path

from ViDE.Toolset import Tool, DownloadUnarchiveConfigureMakeMakeinstall

class BoostPython( Tool ):
    def getDependencies( self ):
        return []

    def getIncludeDirectories( self, context ):
        return []

    def getLibPath( self ):
        return "/"

    def getLibName( self ):
        return "boost_python"
        
class BoostUnitTestFramework( Tool ):
    def getDependencies( self ):
        return []

    def getIncludeDirectories( self, context ):
        return []

    def getLibPath( self ):
        return "/"

    def getLibName( self ):
        return "boost_unit_test_framework"
