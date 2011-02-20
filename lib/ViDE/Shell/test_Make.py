import os.path
import shutil
import unittest
import glob
import time

import ViDE
from ViDE.Core.Action import CompoundException
from ViDE.Shell.Shell import Shell

buildkit = "gcc"

def hppFile( name ):
    return os.path.join( "build", buildkit, "inc", name + ".hpp" )

def objFile( name ):
    return os.path.join( "build", buildkit, "obj", name + ".cpp.o" )

def dllFile( name ):
    return os.path.join( "build", buildkit, "bin", name + ".dll" )

def modFile( name ):
    return os.path.join( "build", buildkit, "pyd", name + ".dll" )

def exeFile( name ):
    return os.path.join( "build", buildkit, "bin", name + ".exe" )

def libFile( name ):
    return os.path.join( "build", buildkit, "lib", "lib" + name + ".a" )

def pyFile( name ):
    return os.path.join( "build", buildkit, "bin", name + ".py" )

def pycFile( name ):
    return os.path.join( "build", buildkit, "pyd", name + ".pyc" )

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
        shell.execute( [ "test", "--silent", "--buildkit", buildkit, "make", "-k" ] )
        time.sleep( 0.5 )
        self.assertFalse( os.path.exists( objFile( "a" ) ) )
        self.assertTrue( os.path.exists( objFile( "b" ) ) )
        self.assertTrue( os.path.exists( objFile( "c" ) ) )
        self.assertTrue( os.path.exists( objFile( "d" ) ) )
        self.assertTrue( os.path.exists( objFile( "e" ) ) )
        self.assertTrue( os.path.exists( objFile( "main" ) ) )
        self.assertFalse( os.path.exists( exeFile( "hello" ) ) )

def TestMake( project, whatIfs ):
    shutil.rmtree( os.path.join( ViDE.rootDirectory, "TestProjects", project, "build" ), True )

    class TestCase( unittest.TestCase ):
        # def __init__( self ):
            # unittest.TestCase.__init__( self )

        def setUp( self ):
            os.chdir( os.path.join( ViDE.rootDirectory, "TestProjects", project ) )
            self.__shell = Shell()
            self.__shell.execute( [ "test", "--silent", "--buildkit", buildkit, "make" ] )
            self.__targets = set()
            for source in whatIfs:
                for target in whatIfs[ source ]:
                    self.__targets.add( target )
    
        def testMake( self ):
            for target in self.__targets:
                self.assertTrue( os.path.exists( target ), project + " " + target )

        def testWhatIf( self ):
            for source in whatIfs:
                before = dict()
                for target in self.__targets:
                    before[ target ] = os.stat( target ).st_mtime
                self.__shell.execute( [ "test", "--buildkit", buildkit, "make", "--touch", "--new-file", source ] )
                after = dict()
                for target in self.__targets:
                    after[ target ] = os.stat( target ).st_mtime

                updatedTargets = set()
                for target in self.__targets:
                    if after[ target ] != before[ target ]:
                        updatedTargets.add( target )
                self.assertEquals( updatedTargets, set( whatIfs[source] ), project + " " + source + " " + str( updatedTargets ) + " != " + str( whatIfs[source] ) )

    return TestCase
            
DynamicLibrary = TestMake( "DynamicLibrary", {
    "lib.cpp": [ dllFile( "hello" ), objFile( "lib" ) ],
    "lib.hpp": [ dllFile( "hello" ), exeFile( "hello" ), hppFile( "lib" ), objFile( "lib" ), objFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), objFile( "main" ) ],
} )

DynamicLibraryDependingOnDynamicLibrary = TestMake( "DynamicLibraryDependingOnDynamicLibrary", {
    "a.cpp": [ dllFile( "a" ), objFile( "a" ) ],
    "a.hpp": [ dllFile( "a" ), dllFile( "b" ), hppFile( "a" ), objFile( "a" ), objFile( "b" ) ],
    "b.cpp": [ dllFile( "b" ), objFile( "b" ) ],
    "b.hpp": [ dllFile( "b" ), exeFile( "hello" ), hppFile( "b" ), objFile( "b" ), objFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), objFile( "main" ) ],
} )

DynamicLibraryDependingOnHeaderLibrary = TestMake( "DynamicLibraryDependingOnHeaderLibrary", {
    "a.hpp": [ dllFile( "b" ), hppFile( "a" ), objFile( "b" ) ],
    "b.cpp": [ dllFile( "b" ), objFile( "b" ) ],
    "b.hpp": [ dllFile( "b" ), exeFile( "hello" ), hppFile( "b" ), objFile( "b" ), objFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), objFile( "main" ) ],
} )

DynamicLibraryDependingOnStaticLibrary = TestMake( "DynamicLibraryDependingOnStaticLibrary", {
    "a.cpp": [ dllFile( "b" ), libFile( "a" ), objFile( "a" ) ],
    "a.hpp": [ dllFile( "b" ), hppFile( "a" ), libFile( "a" ), objFile( "a" ), objFile( "b" ) ],
    "b.cpp": [ dllFile( "b" ), objFile( "b" ) ],
    "b.hpp": [ dllFile( "b" ), exeFile( "hello" ), hppFile( "b" ), objFile( "b" ), objFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), objFile( "main" ) ],
} )

Executable = TestMake( "Executable", {
    "main.cpp": [ exeFile( "hello" ), objFile( "main" ) ],
} )

ExecutableWithManyHeaders = TestMake( "ExecutableWithManyHeaders", {
    "a.cpp": [ exeFile( "hello" ), objFile( "a" ) ],
    "a.hpp": [ exeFile( "hello" ), objFile( "a" ), objFile( "main" ) ],
    "b.cpp": [ exeFile( "hello" ), objFile( "b" ) ],
    "b.hpp": [ exeFile( "hello" ), objFile( "a" ), objFile( "b" ), objFile( "e" ) ],
    "c.cpp": [ exeFile( "hello" ), objFile( "c" ) ],
    "c.hpp": [ exeFile( "hello" ), objFile( "c" ) ],
    "d.cpp": [ exeFile( "hello" ), objFile( "d" ) ],
    "d.hpp": [ exeFile( "hello" ), objFile( "c" ), objFile( "d" ) ],
    "e.cpp": [ exeFile( "hello" ), objFile( "e" ) ],
    "e.hpp": [ exeFile( "hello" ), objFile( "e" ) ],
    "main.cpp": [ exeFile( "hello" ), objFile( "main" ) ],
} )

ExecutableWithManySourceFiles = TestMake( "ExecutableWithManySourceFiles", {
    "a.cpp": [ exeFile( "hello" ), objFile( "a" ) ],
    "b.cpp": [ exeFile( "hello" ), objFile( "b" ) ],
    "c.cpp": [ exeFile( "hello" ), objFile( "c" ) ],
    "d.cpp": [ exeFile( "hello" ), objFile( "d" ) ],
    "e.cpp": [ exeFile( "hello" ), objFile( "e" ) ],
    "main.cpp": [ exeFile( "hello" ), objFile( "main" ) ],
} )

HeaderLibrary = TestMake( "HeaderLibrary", {
    "lib.hpp": [ exeFile( "hello" ), hppFile( "lib" ), objFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), objFile( "main" ) ],
} )

HeaderLibraryDependingOnDynamicLibrary = TestMake( "HeaderLibraryDependingOnDynamicLibrary", {
    "a.cpp": [ dllFile( "a" ), objFile( "a" ) ],
    "a.hpp": [ exeFile( "hello" ), objFile( "main" ), dllFile( "a" ), hppFile( "a" ), objFile( "a" ) ],
    "b.hpp": [ exeFile( "hello" ), hppFile( "b" ), objFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), objFile( "main" ) ],
} )

HeaderLibraryDependingOnHeaderLibrary = TestMake( "HeaderLibraryDependingOnHeaderLibrary", {
    "a.hpp": [ exeFile( "hello" ), objFile( "main" ), hppFile( "a" ) ],
    "b.hpp": [ exeFile( "hello" ), hppFile( "b" ), objFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), objFile( "main" ) ],
} )

HeaderLibraryDependingOnStaticLibrary = TestMake( "HeaderLibraryDependingOnStaticLibrary", {
    "a.cpp": [ exeFile( "hello" ), libFile( "a" ), objFile( "a" ) ],
    "a.hpp": [ exeFile( "hello" ), objFile( "main" ), exeFile( "hello" ), hppFile( "a" ), libFile( "a" ), objFile( "a" ) ],
    "b.hpp": [ exeFile( "hello" ), hppFile( "b" ), objFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), objFile( "main" ) ],
} )

StaticLibrary = TestMake( "StaticLibrary", {
    "lib.cpp": [ exeFile( "hello" ), libFile( "hello" ), objFile( "lib" ) ],
    "lib.hpp": [ exeFile( "hello" ), hppFile( "lib" ), libFile( "hello" ), objFile( "lib" ), objFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), objFile( "main" ) ],
} )

StaticLibraryDependingOnDynamicLibrary = TestMake( "StaticLibraryDependingOnDynamicLibrary", {
    "a.cpp": [ dllFile( "a" ), objFile( "a" ) ],
    "a.hpp": [ dllFile( "a" ), exeFile( "hello" ), hppFile( "a" ), libFile( "b" ), objFile( "a" ), objFile( "b" ) ],
    "b.cpp": [ exeFile( "hello" ), libFile( "b" ), objFile( "b" ) ],
    "b.hpp": [ exeFile( "hello" ), hppFile( "b" ), libFile( "b" ), objFile( "b" ), objFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), objFile( "main" ) ],
} )

StaticLibraryDependingOnHeaderLibrary = TestMake( "StaticLibraryDependingOnHeaderLibrary", {
    "a.hpp": [ exeFile( "hello" ), hppFile( "a" ), libFile( "b" ), objFile( "b" ) ],
    "b.cpp": [ exeFile( "hello" ), libFile( "b" ), objFile( "b" ) ],
    "b.hpp": [ exeFile( "hello" ), hppFile( "b" ), libFile( "b" ), objFile( "b" ), objFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), objFile( "main" ) ],
} )

StaticLibraryDependingOnStaticLibrary = TestMake( "StaticLibraryDependingOnStaticLibrary", {
    "a.cpp": [ exeFile( "hello" ), libFile( "a" ), objFile( "a" ) ],
    "a.hpp": [ exeFile( "hello" ), hppFile( "a" ), libFile( "a" ), libFile( "b" ), objFile( "a" ), objFile( "b" ) ],
    "b.cpp": [ exeFile( "hello" ), libFile( "b" ), objFile( "b" ) ],
    "b.hpp": [ exeFile( "hello" ), hppFile( "b" ), libFile( "b" ), objFile( "b" ), objFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), objFile( "main" ) ],
} )

ComplexCopiedHeadersDependencies = TestMake( "ComplexCopiedHeadersDependencies", {
    "hello1.cpp": [ exeFile( "hello1" ), objFile( "hello1" ) ],
    "hello2.cpp": [ exeFile( "hello2" ), objFile( "hello2" ) ],
    "a.hpp": [ dllFile( "a" ), dllFile( "b" ), exeFile( "hello2" ), hppFile( "a" ), objFile( "a" ), objFile( "b" ), objFile( "hello2" ) ],
    "a1.hpp": [ dllFile( "a" ), dllFile( "b" ), hppFile( "a1" ), objFile( "a" ), objFile( "b" ) ],
    "a2.hpp": [ dllFile( "a" ), dllFile( "b" ), exeFile( "hello2" ), hppFile( "a2" ), objFile( "a" ), objFile( "b" ), objFile( "hello2" ) ],
    "a.cpp": [ dllFile( "a" ), objFile( "a" ) ],
    "b.hpp": [ dllFile( "b" ), exeFile( "hello1" ), exeFile( "hello2" ), hppFile( "b" ), objFile( "b" ), objFile( "hello1" ), objFile( "hello2" ) ],
    "b1.hpp": [ dllFile( "b" ), exeFile( "hello1" ), hppFile( "b1" ), objFile( "b" ), objFile( "hello1" ) ],
    "b2.hpp": [ dllFile( "b" ), exeFile( "hello2" ), hppFile( "b2" ), objFile( "b" ), objFile( "hello2" ) ],
    "b.cpp": [ dllFile( "b" ), objFile( "b" ) ],
} )

ExecutableWithExplicitObjectsAndSources = TestMake( "ExecutableWithExplicitObjectsAndSources", {
    "hello1.cpp": [ exeFile( "hello1" ), objFile( "hello1" ) ],
    "hello2.cpp": [ exeFile( "hello2" ), objFile( "hello2" ) ],
    "hello3.cpp": [ exeFile( "hello3" ), objFile( "hello3" ) ],
    "hello4.cpp": [ exeFile( "hello4" ), objFile( "hello4" ) ],
} )

StaticLibraryWithHeaderStrip = TestMake( "StaticLibraryWithHeaderStrip", {
    "main.cpp": [ objFile( "main" ), exeFile( "hello" ) ],
    os.path.join( "src", "lib.hpp" ): [ objFile( "main" ), exeFile( "hello" ), hppFile( "lib" ), objFile( os.path.join( "src", "lib" ) ), libFile( "hello" ) ],
    os.path.join( "src", "lib.cpp" ): [ exeFile( "hello" ), objFile( os.path.join( "src", "lib" ) ), libFile( "hello" ) ],
    os.path.join( "src", "sub", "sub.hpp" ): [ objFile( "main" ), exeFile( "hello" ), hppFile( os.path.join( "sub", "sub" ) ), objFile( os.path.join( "src", "lib" ) ), libFile( "hello" ) ],
} )

PythonScriptAndModules = TestMake( "PythonScriptAndModules", {
    "hello.py": [ pyFile( "hello" ) ],
    os.path.join( "pack", "b", "__init__.py" ): [ pycFile( os.path.join( "b", "__init__" ) ) ],
    os.path.join( "pack", "b", "b1.py" ): [ pycFile( os.path.join( "b", "b1" ) ) ],
    os.path.join( "pack", "b", "b2.py" ): [ pycFile( os.path.join( "b", "b2" ) ) ],
    "b3.cpp": [ modFile( os.path.join( "b", "b3" ) ) ],
    "a.py": [ pycFile( "a" ) ],
} )

unittest.main()
