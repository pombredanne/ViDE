from gcc import gcc

class gcc_debug( gcc ):
    def getCompilationOptions( self ):
        return [ "-g" ]

    def getLinkOptions( self ):
        return [ "-g" ]
