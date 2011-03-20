import os.path

from ViDE.Core.Loadable import Loadable
from ViDE.ContextReferer import ContextReferer

class Buildkit( Loadable, ContextReferer ):
    def __init__( self, context ):
        Loadable.__init__( self )
        ContextReferer.__init__( self, context )
        
    def fileName( self, *nameParts ):
        return os.path.join( "build", self.name, *nameParts )
