from gcc import gcc

class gcc_release( gcc ):
    def getCompilationOptions( self ):
        return [ "-O3" ]

    def getLinkOptions( self ):
        return []
