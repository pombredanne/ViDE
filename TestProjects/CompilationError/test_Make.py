import os.path
import shutil
import unittest

from ViDE.Core.Action import CompoundException
from ViDE.Shell.Shell import Shell

class TestMake( unittest.TestCase ):
    def test( self ):
        os.chdir( os.path.dirname( __file__ ) )
        shutil.rmtree( "build", True )
        shell = Shell()
        self.assertRaises( CompoundException, shell.execute, [ "test", "make", "-k" ] )
        self.assertFalse( os.path.exists( os.path.join( "build", "gcc", "obj", "a.cpp.o" ) ) )
        self.assertTrue( os.path.exists( os.path.join( "build", "gcc", "obj", "b.cpp.o" ) ) )
        self.assertTrue( os.path.exists( os.path.join( "build", "gcc", "obj", "c.cpp.o" ) ) )
        self.assertTrue( os.path.exists( os.path.join( "build", "gcc", "obj", "d.cpp.o" ) ) )
        self.assertTrue( os.path.exists( os.path.join( "build", "gcc", "obj", "e.cpp.o" ) ) )
        self.assertFalse( os.path.exists( os.path.join( "build", "gcc", "bin", "hello" ) ) )
        shutil.rmtree( "build", True )

unittest.main()