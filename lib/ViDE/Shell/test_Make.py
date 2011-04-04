import os.path
import shutil
import unittest
import time

import ViDE
from ViDE.Shell.Shell import Shell

bkName = "linux_gcc_debug"

def hppFile( name ):
    return os.path.join( "build", bkName, "inc", name + ".hpp" )

def cppObjFile( name ):
    return os.path.join( "build", bkName, "obj", name + ".cpp.o" )

def forObjFile( name ):
    return os.path.join( "build", bkName, "obj", name + ".for.o" )

def dllFile( name ):
    return os.path.join( "build", bkName, "lib", "lib" + name + ".so" )

def modFile( name ):
    return os.path.join( "build", bkName, "pyd", name + ".so" )

def exeFile( name ):
    return os.path.join( "build", bkName, "bin", name )

def libFile( name ):
    return os.path.join( "build", bkName, "lib", "lib" + name + ".a" )

def pyFile( name ):
    return os.path.join( "build", bkName, "bin", name + ".py" )

def pycFile( name ):
    return os.path.join( "build", bkName, "pyd", name + ".pyc" )

def genCppFile( name ):
    return os.path.join( "build", bkName, "gen", name + ".cpp" )

def genHppFile( name ):
    return os.path.join( "build", bkName, "gen", name + ".hpp" )

def genCppObjFile( name ):
    return os.path.join( "build", bkName, "obj", "build", bkName, "gen", name + ".cpp.o" )

def allFilesIn( directory ):
    l = set()
    for path, dirs, files in os.walk( directory ):
        for fileName in files:
            l.add( os.path.join( path, fileName ) )
    return l

class TestCompilationError( unittest.TestCase ):
    def test( self ):
        os.chdir( os.path.join( ViDE.rootDirectory(), "TestProjects", "CompilationError" ) )
        shutil.rmtree( "build", True )
        shell = Shell()
        shell.execute( [ "test", "--silent", "--buildkit", bkName, "make", "-k" ] )
        time.sleep( 0.5 )
        self.assertFalse( os.path.exists( cppObjFile( "a" ) ) )
        self.assertTrue( os.path.exists( cppObjFile( "b" ) ) )
        self.assertTrue( os.path.exists( cppObjFile( "c" ) ) )
        self.assertTrue( os.path.exists( cppObjFile( "d" ) ) )
        self.assertTrue( os.path.exists( cppObjFile( "e" ) ) )
        self.assertTrue( os.path.exists( cppObjFile( "main" ) ) )
        self.assertFalse( os.path.exists( exeFile( "hello" ) ) )

def TestMake( project, whatIfs ):
    shutil.rmtree( os.path.join( ViDE.rootDirectory(), "TestProjects", project, "build" ), True )

    class TestCase( unittest.TestCase ):
        # def __init__( self ):
            # unittest.TestCase.__init__( self )

        def setUp( self ):
            os.chdir( os.path.join( ViDE.rootDirectory(), "TestProjects", project ) )
            self.__shell = Shell()
            self.__shell.execute( [ "test", "--silent", "--buildkit", bkName, "make" ] )
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
                self.__shell.execute( [ "test", "--buildkit", bkName, "make", "--touch", "--new-file", source ] )
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
    "lib.cpp": [ dllFile( "hello" ), cppObjFile( "lib" ) ],
    "lib.hpp": [ dllFile( "hello" ), exeFile( "hello" ), hppFile( "lib" ), cppObjFile( "lib" ), cppObjFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), cppObjFile( "main" ) ],
} )

DynamicLibraryDependingOnDynamicLibrary = TestMake( "DynamicLibraryDependingOnDynamicLibrary", {
    "a.cpp": [ dllFile( "a" ), cppObjFile( "a" ) ],
    "a.hpp": [ dllFile( "a" ), dllFile( "b" ), hppFile( "a" ), cppObjFile( "a" ), cppObjFile( "b" ) ],
    "b.cpp": [ dllFile( "b" ), cppObjFile( "b" ) ],
    "b.hpp": [ dllFile( "b" ), exeFile( "hello" ), hppFile( "b" ), cppObjFile( "b" ), cppObjFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), cppObjFile( "main" ) ],
} )

DynamicLibraryDependingOnHeaderLibrary = TestMake( "DynamicLibraryDependingOnHeaderLibrary", {
    "a.hpp": [ dllFile( "b" ), hppFile( "a" ), cppObjFile( "b" ) ],
    "b.cpp": [ dllFile( "b" ), cppObjFile( "b" ) ],
    "b.hpp": [ dllFile( "b" ), exeFile( "hello" ), hppFile( "b" ), cppObjFile( "b" ), cppObjFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), cppObjFile( "main" ) ],
} )

DynamicLibraryDependingOnStaticLibrary = TestMake( "DynamicLibraryDependingOnStaticLibrary", {
    "a.cpp": [ dllFile( "b" ), libFile( "a" ), cppObjFile( "a" ) ],
    "a.hpp": [ dllFile( "b" ), hppFile( "a" ), libFile( "a" ), cppObjFile( "a" ), cppObjFile( "b" ) ],
    "b.cpp": [ dllFile( "b" ), cppObjFile( "b" ) ],
    "b.hpp": [ dllFile( "b" ), exeFile( "hello" ), hppFile( "b" ), cppObjFile( "b" ), cppObjFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), cppObjFile( "main" ) ],
} )

Executable = TestMake( "Executable", {
    "main.cpp": [ exeFile( "hello" ), cppObjFile( "main" ) ],
} )

ExecutableWithManyHeaders = TestMake( "ExecutableWithManyHeaders", {
    "a.cpp": [ exeFile( "hello" ), cppObjFile( "a" ) ],
    "a.hpp": [ exeFile( "hello" ), cppObjFile( "a" ), cppObjFile( "main" ) ],
    "b.cpp": [ exeFile( "hello" ), cppObjFile( "b" ) ],
    "b.hpp": [ exeFile( "hello" ), cppObjFile( "a" ), cppObjFile( "b" ), cppObjFile( "e" ) ],
    "c.cpp": [ exeFile( "hello" ), cppObjFile( "c" ) ],
    "c.hpp": [ exeFile( "hello" ), cppObjFile( "c" ) ],
    "d.cpp": [ exeFile( "hello" ), cppObjFile( "d" ) ],
    "d.hpp": [ exeFile( "hello" ), cppObjFile( "c" ), cppObjFile( "d" ) ],
    "e.cpp": [ exeFile( "hello" ), cppObjFile( "e" ) ],
    "e.hpp": [ exeFile( "hello" ), cppObjFile( "e" ) ],
    "main.cpp": [ exeFile( "hello" ), cppObjFile( "main" ) ],
} )

ExecutableWithManySourceFiles = TestMake( "ExecutableWithManySourceFiles", {
    "a.cpp": [ exeFile( "hello" ), cppObjFile( "a" ) ],
    "b.cpp": [ exeFile( "hello" ), cppObjFile( "b" ) ],
    "c.cpp": [ exeFile( "hello" ), cppObjFile( "c" ) ],
    "d.cpp": [ exeFile( "hello" ), cppObjFile( "d" ) ],
    "e.cpp": [ exeFile( "hello" ), cppObjFile( "e" ) ],
    "main.cpp": [ exeFile( "hello" ), cppObjFile( "main" ) ],
} )

HeaderLibrary = TestMake( "HeaderLibrary", {
    "lib.hpp": [ exeFile( "hello" ), hppFile( "lib" ), cppObjFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), cppObjFile( "main" ) ],
} )

HeaderLibraryDependingOnDynamicLibrary = TestMake( "HeaderLibraryDependingOnDynamicLibrary", {
    "a.cpp": [ dllFile( "a" ), cppObjFile( "a" ) ],
    "a.hpp": [ exeFile( "hello" ), cppObjFile( "main" ), dllFile( "a" ), hppFile( "a" ), cppObjFile( "a" ) ],
    "b.hpp": [ exeFile( "hello" ), hppFile( "b" ), cppObjFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), cppObjFile( "main" ) ],
} )

HeaderLibraryDependingOnHeaderLibrary = TestMake( "HeaderLibraryDependingOnHeaderLibrary", {
    "a.hpp": [ exeFile( "hello" ), cppObjFile( "main" ), hppFile( "a" ) ],
    "b.hpp": [ exeFile( "hello" ), hppFile( "b" ), cppObjFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), cppObjFile( "main" ) ],
} )

HeaderLibraryDependingOnStaticLibrary = TestMake( "HeaderLibraryDependingOnStaticLibrary", {
    "a.cpp": [ exeFile( "hello" ), libFile( "a" ), cppObjFile( "a" ) ],
    "a.hpp": [ exeFile( "hello" ), cppObjFile( "main" ), exeFile( "hello" ), hppFile( "a" ), libFile( "a" ), cppObjFile( "a" ) ],
    "b.hpp": [ exeFile( "hello" ), hppFile( "b" ), cppObjFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), cppObjFile( "main" ) ],
} )

StaticLibrary = TestMake( "StaticLibrary", {
    "lib.cpp": [ exeFile( "hello" ), libFile( "hello" ), cppObjFile( "lib" ) ],
    "lib.hpp": [ exeFile( "hello" ), hppFile( "lib" ), libFile( "hello" ), cppObjFile( "lib" ), cppObjFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), cppObjFile( "main" ) ],
} )

StaticLibraryDependingOnDynamicLibrary = TestMake( "StaticLibraryDependingOnDynamicLibrary", {
    "a.cpp": [ dllFile( "a" ), cppObjFile( "a" ) ],
    "a.hpp": [ dllFile( "a" ), exeFile( "hello" ), hppFile( "a" ), libFile( "b" ), cppObjFile( "a" ), cppObjFile( "b" ) ],
    "b.cpp": [ exeFile( "hello" ), libFile( "b" ), cppObjFile( "b" ) ],
    "b.hpp": [ exeFile( "hello" ), hppFile( "b" ), libFile( "b" ), cppObjFile( "b" ), cppObjFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), cppObjFile( "main" ) ],
} )

StaticLibraryDependingOnHeaderLibrary = TestMake( "StaticLibraryDependingOnHeaderLibrary", {
    "a.hpp": [ exeFile( "hello" ), hppFile( "a" ), libFile( "b" ), cppObjFile( "b" ) ],
    "b.cpp": [ exeFile( "hello" ), libFile( "b" ), cppObjFile( "b" ) ],
    "b.hpp": [ exeFile( "hello" ), hppFile( "b" ), libFile( "b" ), cppObjFile( "b" ), cppObjFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), cppObjFile( "main" ) ],
} )

StaticLibraryDependingOnStaticLibrary = TestMake( "StaticLibraryDependingOnStaticLibrary", {
    "a.cpp": [ exeFile( "hello" ), libFile( "a" ), cppObjFile( "a" ) ],
    "a.hpp": [ exeFile( "hello" ), hppFile( "a" ), libFile( "a" ), libFile( "b" ), cppObjFile( "a" ), cppObjFile( "b" ) ],
    "b.cpp": [ exeFile( "hello" ), libFile( "b" ), cppObjFile( "b" ) ],
    "b.hpp": [ exeFile( "hello" ), hppFile( "b" ), libFile( "b" ), cppObjFile( "b" ), cppObjFile( "main" ) ],
    "main.cpp": [ exeFile( "hello" ), cppObjFile( "main" ) ],
} )

ComplexCopiedHeadersDependencies = TestMake( "ComplexCopiedHeadersDependencies", {
    "hello1.cpp": [ exeFile( "hello1" ), cppObjFile( "hello1" ) ],
    "hello2.cpp": [ exeFile( "hello2" ), cppObjFile( "hello2" ) ],
    "a.hpp": [ dllFile( "a" ), dllFile( "b" ), exeFile( "hello2" ), hppFile( "a" ), cppObjFile( "a" ), cppObjFile( "b" ), cppObjFile( "hello2" ) ],
    "a1.hpp": [ dllFile( "a" ), dllFile( "b" ), hppFile( "a1" ), cppObjFile( "a" ), cppObjFile( "b" ) ],
    "a2.hpp": [ dllFile( "a" ), dllFile( "b" ), exeFile( "hello2" ), hppFile( "a2" ), cppObjFile( "a" ), cppObjFile( "b" ), cppObjFile( "hello2" ) ],
    "a.cpp": [ dllFile( "a" ), cppObjFile( "a" ) ],
    "b.hpp": [ dllFile( "b" ), exeFile( "hello1" ), exeFile( "hello2" ), hppFile( "b" ), cppObjFile( "b" ), cppObjFile( "hello1" ), cppObjFile( "hello2" ) ],
    "b1.hpp": [ dllFile( "b" ), exeFile( "hello1" ), hppFile( "b1" ), cppObjFile( "b" ), cppObjFile( "hello1" ) ],
    "b2.hpp": [ dllFile( "b" ), exeFile( "hello2" ), hppFile( "b2" ), cppObjFile( "b" ), cppObjFile( "hello2" ) ],
    "b.cpp": [ dllFile( "b" ), cppObjFile( "b" ) ],
} )

ExecutableWithExplicitObjectsAndSources = TestMake( "ExecutableWithExplicitObjectsAndSources", {
    "hello1.cpp": [ exeFile( "hello1" ), cppObjFile( "hello1" ) ],
    "hello2.cpp": [ exeFile( "hello2" ), cppObjFile( "hello2" ) ],
    "hello3.cpp": [ exeFile( "hello3" ), cppObjFile( "hello3" ) ],
    "hello4.cpp": [ exeFile( "hello4" ), cppObjFile( "hello4" ) ],
} )

StaticLibraryWithHeaderStrip = TestMake( "StaticLibraryWithHeaderStrip", {
    "main.cpp": [ cppObjFile( "main" ), exeFile( "hello" ) ],
    os.path.join( "src", "lib.hpp" ): [ cppObjFile( "main" ), exeFile( "hello" ), hppFile( "lib" ), cppObjFile( os.path.join( "src", "lib" ) ), libFile( "hello" ) ],
    os.path.join( "src", "lib.cpp" ): [ exeFile( "hello" ), cppObjFile( os.path.join( "src", "lib" ) ), libFile( "hello" ) ],
    os.path.join( "src", "sub", "sub.hpp" ): [ cppObjFile( "main" ), exeFile( "hello" ), hppFile( os.path.join( "sub", "sub" ) ), cppObjFile( os.path.join( "src", "lib" ) ), libFile( "hello" ) ],
} )

PythonScriptAndModules = TestMake( "PythonScriptAndModules", {
    "hello.py": [ pyFile( "hello" ) ],
    os.path.join( "pack", "b", "__init__.py" ): [ pycFile( os.path.join( "b", "__init__" ) ) ],
    os.path.join( "pack", "b", "b1.py" ): [ pycFile( os.path.join( "b", "b1" ) ) ],
    os.path.join( "pack", "b", "b2.py" ): [ pycFile( os.path.join( "b", "b2" ) ) ],
    "b3.cpp": [ modFile( os.path.join( "b", "b3" ) ) ],
    "a.py": [ pycFile( "a" ) ],
} )

FortranExecutable = TestMake( "FortranExecutable", {
    "main.for": [ exeFile( "hello" ), forObjFile( "main" ) ],
    "sub.for": [ exeFile( "hello" ), forObjFile( "sub" ) ],
} )

FortranCalledFromCpp = TestMake( "FortranCalledFromCpp", {
    "main.cpp": [ exeFile( "hello" ), cppObjFile( "main" ) ],
    "sub.for": [ exeFile( "hello" ), forObjFile( "sub" ) ],
} )

ExecutableWithGeneratedSources = TestMake( "ExecutableWithGeneratedSources", {
    "main.cpp": [ exeFile( "hello" ), cppObjFile( "main" ) ],
    "a.xsd": [ genCppFile( "a.xsd" ), genHppFile( "a.xsd" ), genCppObjFile( "a.xsd" ), exeFile( "hello" ) ]
} )

ExecutableWithExternalDependency = TestMake( "ExecutableWithExternalDependency", {
    "main.cpp": [ exeFile( "hello" ), cppObjFile( "main" ) ],
} )

MoreComplexCopiedHeadersDependencies = TestMake( "MoreComplexCopiedHeadersDependencies", {
    "main.cpp": [ exeFile( "hello" ), cppObjFile( "main" ) ],
    "src/lib.hpp": [ exeFile( "hello" ), cppObjFile( "main" ), hppFile( "lib" ) ],
    "src/lib/a.hpp": [ exeFile( "hello" ), cppObjFile( "main" ), hppFile( "lib/a" ) ],
    "src/lib/b.hpp": [ exeFile( "hello" ), cppObjFile( "main" ), hppFile( "lib/b" ) ],
    "src/lib.cpp": [ dllFile( "lib" ), cppObjFile( "src/lib" ), cppObjFile( "src/lib" ) ],
} )

unittest.main()
