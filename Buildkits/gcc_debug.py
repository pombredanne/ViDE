class gcc_debug:
    def getFlavourCompilationOptions( self ):
        return [ "-g" ]

    def getLinkOptions( self ):
        return [ "-g" ]
