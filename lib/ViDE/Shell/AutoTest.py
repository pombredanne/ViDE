import os
import fnmatch

import ViDE
from Misc.InteractiveCommandLineProgram import Command

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
            self.__testsToRun = self.__testFiles
        else:
            self.__testsToRun = set()
            for arg in args:
                if os.path.realpath( arg ) in self.__testFiles:
                    self.__testsToRun.add( arg )
                elif arg in [ os.path.basename( f ) for f in self.__testFiles ]:
                    for f in self.__testFiles:
                        if arg == os.path.basename( f ):
                            self.__testsToRun.add( f )
                elif "test_" + arg + ".py" in [ os.path.basename( f ) for f in self.__testFiles ]:
                    for f in self.__testFiles:
                        if "test_" + arg + ".py" == os.path.basename( f ):
                            self.__testsToRun.add( f )
                else:
                    raise Exception( "Incorrect argument " + arg )
        self.__testsToRun = sorted( self.__testsToRun )
    
    def __runTests( self ):
        for test in self.__testsToRun:
            self.__runTest( test )
    
    def __runTest( self, test ):
        ### @todo Refactor
        print test
        os.environ[ "PYTHONPATH" ] = ViDE.libDirectory
        os.system( "python " + test + " -q" )
        print
