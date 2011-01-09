import subprocess

from ViDE.Core.Action import Action
from ViDE import Log

class SystemAction( Action ):
    def __init__( self, command, preview ):
        Action.__init__( self )
        self.__command = command
        self.__preview = preview
    
    def doPreview( self ):
        return self.__preview
        
    def doExecute( self ):
        Log.info( self.__preview )
        subprocess.check_call( self.__command )
        Log.verbose( "End of", self.__preview )
