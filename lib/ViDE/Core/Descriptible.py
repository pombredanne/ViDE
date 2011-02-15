import imp

class Descriptible:
    def __init__( self ):
        pass

    @classmethod
    def loadFromDescription( cls, descriptionFile, *args, **kwargs ):
        instance = cls( *args, **kwargs )

        #print "Loading", cls.__name__, "from", descriptionFile

        cls.inProgress = instance
        imp.load_source( "description", descriptionFile )
        del cls.inProgress

        return instance
