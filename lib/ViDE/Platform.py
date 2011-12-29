from ViDE.Core.Loadable import Loadable
from ViDE.ContextReferer import ContextReferer

class Platform( Loadable, ContextReferer ):
    def __init__( self, context ):
        Loadable.__init__( self )
        ContextReferer.__init__( self, context )
