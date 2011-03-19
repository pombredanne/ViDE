from gcc import gcc

class gcc_test( gcc ):
    def getCompilationOptions( self ):
        return [ "-g", "--coverage" ]

    def getLinkOptions( self ):
        return [ "-g", "--coverage" ]
