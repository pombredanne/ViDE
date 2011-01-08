import os

from ViDE.Core.Action import Action

class SystemAction( Action ):
    def __init__( self, command, preview ):
        Action.__init__( self )
        self.__command = command
        self.__preview = preview
    
    def doPreview( self ):
        return self.__preview
        
    def doExecute( self ):
        os.system( self.__command )
