import imp
import os.path

import ViDE
from ViDE.Core.Loadable import Loadable

class Buildkit( Loadable ):
    def __init__( self ):
        Loadable.__init__( self )
        
    def fileName( self, *nameParts ):
        return os.path.join( "build", self.name, *( self.getPreliminaryNameParts() + list( nameParts ) ) )
