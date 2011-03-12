from ViDE.Toolset import Toolset

from Cairo import Pixman, Cairo, Cairomm, PyCairo

class ts20110308( Toolset ):
    def computeTools( self ):
        return [
            Pixman( "0.21.6" ),
            Cairo( "1.10.2" ),
            Cairomm( "1.9.8" ),
            PyCairo( "1.8.10" )
        ]
