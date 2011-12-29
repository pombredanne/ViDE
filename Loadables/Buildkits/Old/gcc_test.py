class gcc_test:
    def getFlavourCompilationOptions( self ):
        return [ "-g", "--coverage" ]

    def getLinkOptions( self ):
        return [ "-g", "--coverage" ]
