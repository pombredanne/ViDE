from ViDE.Core.Loadable import Loadable
from ViDE.ContextReferer import ContextReferer

class Flavour( Loadable, ContextReferer ):
    def __init__( self, context ):
        Loadable.__init__( self )
        ContextReferer.__init__( self, context )
