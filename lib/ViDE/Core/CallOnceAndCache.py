class CallOnceAndCache:
    def __init__( self ):
        self.__cachedValues = dict()

    def getCached( self, key, function, *args, **kwargs ):
        key += "#" + "*".join( str( arg ) for arg in args )
        key += "#" + "*".join( str( k ) + ":" + str( kwargs[ k ] ) for k in kwargs )
        if not self.__cachedValues.has_key( key ):
            self.__cachedValues[ key ] = function( *args, **kwargs )
        return self.__cachedValues[ key ]
