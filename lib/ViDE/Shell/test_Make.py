import os.path
import shutil
import unittest
import glob
import time

import ViDE
from ViDE.Core.Action import CompoundException
from ViDE.Shell.Shell import Shell

def allFilesIn( directory ):
    l = set()
    for path, dirs, files in os.walk( directory ):
        for fileName in files:
            l.add( os.path.join( path, fileName ) )
    return l

class TestCompilationError( unittest.TestCase ):
    def test( self ):
        os.chdir( os.path.join( ViDE.rootDirectory, "TestProjects", "CompilationError" ) )
        shutil.rmtree( "build", True )
        shell = Shell()
        shell.execute( [ "test", "--silent", "--buildkit", "gcc", "make", "-k" ] )
        self.assertFalse( os.path.exists( os.path.join( "build", "gcc", "obj", "a.cpp.o" ) ) )
        self.assertTrue( os.path.exists( os.path.join( "build", "gcc", "obj", "b.cpp.o" ) ) )
        self.assertTrue( os.path.exists( os.path.join( "build", "gcc", "obj", "c.cpp.o" ) ) )
        self.assertTrue( os.path.exists( os.path.join( "build", "gcc", "obj", "d.cpp.o" ) ) )
        self.assertTrue( os.path.exists( os.path.join( "build", "gcc", "obj", "e.cpp.o" ) ) )
        self.assertFalse( os.path.exists( os.path.join( "build", "gcc", "bin", "hello" ) ) )

def TestMake( project, whatIfs ):
    shutil.rmtree( os.path.join( ViDE.rootDirectory, "TestProjects", project, "build" ), True )

    class TestCase( unittest.TestCase ):
        # def __init__( self ):
            # unittest.TestCase.__init__( self )

        def setUp( self ):
            os.chdir( os.path.join( ViDE.rootDirectory, "TestProjects", project ) )
            self.__shell = Shell()
            self.__shell.execute( [ "test", "--silent", "--buildkit", "gcc", "make" ] )
    
        def testMake( self ):
            self.assertTrue( os.path.exists( os.path.join( "build", "gcc", "bin", "hello" ) ) )

        def testWhatIf( self ):
            targets = allFilesIn( os.path.join( "build", "gcc" ) )
            targets.remove( os.path.join( "build", "gcc", "report.png" ) )

            for source in whatIfs:
                before = dict()
                for target in targets:
                    before[ target ] = os.stat( target ).st_mtime
                time.sleep( 0.1 )
                self.__shell.execute( [ "test", "--buildkit", "gcc", "make", "-t", "--new-file", source ] )
                after = dict()
                for target in targets:
                    after[ target ] = os.stat( target ).st_mtime

                updatedTargets = set()
                for target in targets:
                    if after[ target ] != before[ target ]:
                        updatedTargets.add( target )
                self.assertEquals( updatedTargets, whatIfs[source] )

    return TestCase
            
DynamicLibrary = TestMake( "DynamicLibrary", {
    "lib.cpp": set( [ "build/gcc/bin/hello.dll", "build/gcc/obj/lib.cpp.o", ] ),
    "lib.hpp": set( [ "build/gcc/bin/hello.dll", "build/gcc/bin/hello.exe", "build/gcc/inc/lib.hpp", "build/gcc/obj/lib.cpp.o", "build/gcc/obj/main.cpp.o", ] ),
    "main.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/main.cpp.o", ] ),
} )

DynamicLibraryDependingOnDynamicLibrary = TestMake( "DynamicLibraryDependingOnDynamicLibrary", {
    "a.cpp": set( [ "build/gcc/bin/a.dll", "build/gcc/obj/a.cpp.o", ] ),
    "a.hpp": set( [ "build/gcc/bin/a.dll", "build/gcc/bin/b.dll", "build/gcc/bin/hello.exe", "build/gcc/inc/a.hpp", "build/gcc/obj/a.cpp.o", "build/gcc/obj/b.cpp.o", ] ),
    "b.cpp": set( [ "build/gcc/bin/b.dll", "build/gcc/obj/b.cpp.o", ] ),
    "b.hpp": set( [ "build/gcc/bin/b.dll", "build/gcc/bin/hello.exe", "build/gcc/inc/b.hpp", "build/gcc/obj/b.cpp.o", "build/gcc/obj/main.cpp.o", ] ),
    "main.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/main.cpp.o", ] ),
} )

DynamicLibraryDependingOnHeaderLibrary = TestMake( "DynamicLibraryDependingOnHeaderLibrary", {
    "a.hpp": set( [ "build/gcc/bin/b.dll", "build/gcc/bin/hello.exe", "build/gcc/inc/a.hpp", "build/gcc/obj/b.cpp.o", ] ),
    "b.cpp": set( [ "build/gcc/bin/b.dll", "build/gcc/obj/b.cpp.o", ] ),
    "b.hpp": set( [ "build/gcc/bin/b.dll", "build/gcc/bin/hello.exe", "build/gcc/inc/b.hpp", "build/gcc/obj/b.cpp.o", "build/gcc/obj/main.cpp.o", ] ),
    "main.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/main.cpp.o", ] ),
} )

DynamicLibraryDependingOnStaticLibrary = TestMake( "DynamicLibraryDependingOnStaticLibrary", {
    "a.cpp": set( [ "build/gcc/bin/b.dll", "build/gcc/lib/liba.a", "build/gcc/obj/a.cpp.o", ] ),
    "a.hpp": set( [ "build/gcc/bin/b.dll", "build/gcc/bin/hello.exe", "build/gcc/inc/a.hpp", "build/gcc/lib/liba.a", "build/gcc/obj/a.cpp.o", "build/gcc/obj/b.cpp.o", ] ),
    "b.cpp": set( [ "build/gcc/bin/b.dll", "build/gcc/obj/b.cpp.o", ] ),
    "b.hpp": set( [ "build/gcc/bin/b.dll", "build/gcc/bin/hello.exe", "build/gcc/inc/b.hpp", "build/gcc/obj/b.cpp.o", "build/gcc/obj/main.cpp.o", ] ),
    "main.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/main.cpp.o", ] ),
} )

Executable = TestMake( "Executable", {
    "main.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/main.cpp.o", ] ),
} )

ExecutableWithManyHeaders = TestMake( "ExecutableWithManyHeaders", {
    "a.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/a.cpp.o", ] ),
    "a.hpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/a.cpp.o", "build/gcc/obj/main.cpp.o", ] ),
    "b.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/b.cpp.o", ] ),
    "b.hpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/a.cpp.o", "build/gcc/obj/b.cpp.o", "build/gcc/obj/e.cpp.o", ] ),
    "c.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/c.cpp.o", ] ),
    "c.hpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/c.cpp.o", ] ),
    "d.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/d.cpp.o", ] ),
    "d.hpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/c.cpp.o", "build/gcc/obj/d.cpp.o", ] ),
    "e.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/e.cpp.o", ] ),
    "e.hpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/e.cpp.o", ] ),
    "main.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/main.cpp.o", ] ),
} )

ExecutableWithManySourceFiles = TestMake( "ExecutableWithManySourceFiles", {
    "a.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/a.cpp.o", ] ),
    "b.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/b.cpp.o", ] ),
    "c.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/c.cpp.o", ] ),
    "d.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/d.cpp.o", ] ),
    "e.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/e.cpp.o", ] ),
    "main.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/main.cpp.o", ] ),
} )

HeaderLibrary = TestMake( "HeaderLibrary", {
    "lib.hpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/inc/lib.hpp", "build/gcc/obj/main.cpp.o", ] ),
    "main.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/main.cpp.o", ] ),
} )

HeaderLibraryDependingOnDynamicLibrary = TestMake( "HeaderLibraryDependingOnDynamicLibrary", {
    "a.cpp": set( [ "build/gcc/bin/a.dll", "build/gcc/obj/a.cpp.o", ] ),
    "a.hpp": set( [ "build/gcc/bin/a.dll", "build/gcc/bin/hello.exe", "build/gcc/inc/a.hpp", "build/gcc/obj/a.cpp.o", ] ),
    "b.hpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/inc/b.hpp", "build/gcc/obj/main.cpp.o", ] ),
    "main.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/main.cpp.o", ] ),
} )

HeaderLibraryDependingOnHeaderLibrary = TestMake( "HeaderLibraryDependingOnHeaderLibrary", {
    "a.hpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/inc/a.hpp", ] ),
    "b.hpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/inc/b.hpp", "build/gcc/obj/main.cpp.o", ] ),
    "main.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/main.cpp.o", ] ),
} )

HeaderLibraryDependingOnStaticLibrary = TestMake( "HeaderLibraryDependingOnStaticLibrary", {
    "a.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/lib/liba.a", "build/gcc/obj/a.cpp.o", ] ),
    "a.hpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/inc/a.hpp", "build/gcc/lib/liba.a", "build/gcc/obj/a.cpp.o", ] ),
    "b.hpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/inc/b.hpp", "build/gcc/obj/main.cpp.o", ] ),
    "main.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/main.cpp.o", ] ),
} )

StaticLibrary = TestMake( "StaticLibrary", {
    "lib.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/lib/libhello.a", "build/gcc/obj/lib.cpp.o", ] ),
    "lib.hpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/inc/lib.hpp", "build/gcc/lib/libhello.a", "build/gcc/obj/lib.cpp.o", "build/gcc/obj/main.cpp.o", ] ),
    "main.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/main.cpp.o", ] ),
} )

StaticLibraryDependingOnDynamicLibrary = TestMake( "StaticLibraryDependingOnDynamicLibrary", {
    "a.cpp": set( [ "build/gcc/bin/a.dll", "build/gcc/obj/a.cpp.o", ] ),
    "a.hpp": set( [ "build/gcc/bin/a.dll", "build/gcc/bin/hello.exe", "build/gcc/inc/a.hpp", "build/gcc/lib/libb.a", "build/gcc/obj/a.cpp.o", "build/gcc/obj/b.cpp.o", ] ),
    "b.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/lib/libb.a", "build/gcc/obj/b.cpp.o", ] ),
    "b.hpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/inc/b.hpp", "build/gcc/lib/libb.a", "build/gcc/obj/b.cpp.o", "build/gcc/obj/main.cpp.o", ] ),
    "main.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/main.cpp.o", ] ),
} )

StaticLibraryDependingOnHeaderLibrary = TestMake( "StaticLibraryDependingOnHeaderLibrary", {
    "a.hpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/inc/a.hpp", "build/gcc/lib/libb.a", "build/gcc/obj/b.cpp.o", ] ),
    "b.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/lib/libb.a", "build/gcc/obj/b.cpp.o", ] ),
    "b.hpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/inc/b.hpp", "build/gcc/lib/libb.a", "build/gcc/obj/b.cpp.o", "build/gcc/obj/main.cpp.o", ] ),
    "main.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/main.cpp.o", ] ),
} )

StaticLibraryDependingOnStaticLibrary  = TestMake( "StaticLibraryDependingOnStaticLibrary", {
    "a.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/lib/liba.a", "build/gcc/obj/a.cpp.o", ] ),
    "a.hpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/inc/a.hpp", "build/gcc/lib/liba.a", "build/gcc/lib/libb.a", "build/gcc/obj/a.cpp.o", "build/gcc/obj/b.cpp.o", ] ),
    "b.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/lib/libb.a", "build/gcc/obj/b.cpp.o", ] ),
    "b.hpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/inc/b.hpp", "build/gcc/lib/libb.a", "build/gcc/obj/b.cpp.o", "build/gcc/obj/main.cpp.o", ] ),
    "main.cpp": set( [ "build/gcc/bin/hello.exe", "build/gcc/obj/main.cpp.o", ] ),
} )

unittest.main()
