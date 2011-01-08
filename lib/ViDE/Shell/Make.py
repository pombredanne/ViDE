from Misc import InteractiveCommandLineProgram

from ViDE.Project.Project import Project

class Make( InteractiveCommandLineProgram.Command ):
    def __init__( self, program ):
        InteractiveCommandLineProgram.Command.__init__( self, program )
        self.jobs = 1
        self.addOption( "j", "jobs", InteractiveCommandLineProgram.StoreArgument( "JOBS" ), "use JOBS parallel jobs" )

    def execute( self, args ):
        action = Project.load( "videfile.py" ).getBuildAction()
        action.execute( False, self.jobs )
