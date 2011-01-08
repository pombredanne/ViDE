from Misc.InteractiveCommandLineProgram import Command

from ViDE.Project.Project import Project

class Make( Command ):
    def execute( self, args ):
        action = Project.load( "videfile.py" ).getBuildAction()
        print action.preview()
