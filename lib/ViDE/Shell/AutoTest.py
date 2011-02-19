import os
import fnmatch

import ViDE
from Misc.InteractiveCommandLineProgram import Command

class Test:
    def __init__( self, file, test ):
        self.file = file
        self.test = test

class AutoTest( Command ):
    ### @todo Measure test coverage
    ### @todo Discover missing test files, base on python files *.py without a test_*.py
    def execute( self, args ):
        self.__listTestFiles()
        self.__selectTestsToRun( args )
        self.__runTests()
    
    def __listTestFiles( self ):
        self.__testFiles = []
        for path, dirs, files in os.walk( ViDE.rootDirectory ):
            for fileName in fnmatch.filter( files, "test_*.py" ):
                self.__testFiles.append( os.path.realpath( os.path.join( path, fileName ) ) )

    def __selectTestsToRun( self, args ):
        ### @todo Refactor
        ### @todo Allow arguments of form Filename.Classname.testMethod => python Filename Classname.testMethod
        if len( args ) == 0:
            self.__testsToRun = [ Test( file, None ) for file in self.__testFiles ]
        else:
            self.__testsToRun = set()
            for arg in args:
                fileAndTest = arg.split( ".", 1 )
                if len( fileAndTest ) == 2:
                    file, test = fileAndTest
                else:
                    file = fileAndTest[ 0 ]
                    test = None
                for f in self.__testFiles:
                    if "test_" + file + ".py" == os.path.basename( f ):
                        self.__testsToRun.add( Test( f, test ) )
        self.__testsToRun = sorted( self.__testsToRun, key = lambda test: ( test.file, test.test ) )
    
    def __runTests( self ):
        for test in self.__testsToRun:
            self.__runTest( test )
    
    def __runTest( self, test ):
        ### @todo Refactor
        os.environ[ "PYTHONPATH" ] = ViDE.libDirectory
        if test.test:
            print test.file, test.test
            os.system( "python " + test.file + " -q " + test.test )
        else:
            print test.file
            os.system( "python " + test.file + " -q " )
        print
