import os

from ViDE.Core.Action import Action

class SystemAction( Action ):
    def __init__( self, command ):
        Action.__init__( self )
        self.__command = command
    
    def doPreview( self ):
        return self.__command
        
    def doExecute( self ):
        print self.__command
        os.system( self.__command )