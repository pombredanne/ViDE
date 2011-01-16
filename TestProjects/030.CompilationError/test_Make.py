import os.path
import shutil
import unittest

import ViDE.Core.Action
from ViDE.Shell.Make import Make

class TestMake( unittest.TestCase ):
    def test( self ):
        os.chdir( os.path.dirname( __file__ ) )
        shutil.rmtree( "build", True )
        make = Make( None )
        make.keepGoing = True
        make.execute( [] )
        self.assertFalse( os.path.exists( os.path.join( "build", "obj", "a.cpp.o" ) ) )
        self.assertTrue( os.path.exists( os.path.join( "build", "obj", "b.cpp.o" ) ) )
        self.assertTrue( os.path.exists( os.path.join( "build", "obj", "c.cpp.o" ) ) )
        self.assertTrue( os.path.exists( os.path.join( "build", "obj", "d.cpp.o" ) ) )
        self.assertTrue( os.path.exists( os.path.join( "build", "obj", "e.cpp.o" ) ) )
        self.assertFalse( os.path.exists( os.path.join( "build", "bin", "hello" ) ) )
        shutil.rmtree( "build", True )

if __name__ == "__main__":
    unittest.main()