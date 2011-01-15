import os.path
import shutil
import unittest

from ViDE.Shell.Make import Make

class TestMake( unittest.TestCase ):
    def test( self ):
        os.chdir( os.path.dirname( __file__ ) )
        shutil.rmtree( "build", True )
        make = Make( None )
        make.execute( [] )
        self.assertTrue( os.path.exists( os.path.join( "build", "bin", "hello" ) ) )
        shutil.rmtree( "build", True )

if __name__ == "__main__":
    unittest.main()
