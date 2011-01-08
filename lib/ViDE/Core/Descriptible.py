import imp

class Descriptible:
    @classmethod
    def load( cls, descriptionFile ):
        instance = cls()

        #print "Loading", cls.__name__, "from", descriptionFile

        cls.inProgress = instance
        instance.beginDescription()
        imp.load_source( "description", descriptionFile )
        instance.endDescription()
        del cls.inProgress

        return instance
