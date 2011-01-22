import os.path
import shutil
import unittest

from ViDE.Shell.Shell import Shell

class TestMake( unittest.TestCase ):
    def test( self ):
        os.chdir( os.path.dirname( __file__ ) )
        shutil.rmtree( "build", True )
        shell = Shell()
        shell.execute( [ "test", "make" ] )
        self.assertTrue( os.path.exists( os.path.join( "build", "bin", "hello" ) ) )
        shutil.rmtree( "build", True )

unittest.main()
