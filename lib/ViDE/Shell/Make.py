from Misc import InteractiveCommandLineProgram

from ViDE.Project.Project import Project

class Make( InteractiveCommandLineProgram.Command ):
    def __init__( self, program ):
        InteractiveCommandLineProgram.Command.__init__( self, program )
        self.jobs = 1
        self.addOption( [ "j", "jobs" ], "jobs", InteractiveCommandLineProgram.StoreArgument( "JOBS" ), "use JOBS parallel jobs" )
        self.keepGoing = False
        self.addOption( [ "k", "keep-going" ], "keepGoing", InteractiveCommandLineProgram.StoreConstant( True ), "keep going in case of failure" )
        self.dryRun = False
        self.addOption( [ "n", "dry-run" ], "dryRun", InteractiveCommandLineProgram.StoreConstant( True ), "print commands instead of executing them" )
        

    def execute( self, args ):
        action = Project.load( "videfile.py" ).getBuildAction()
        if self.dryRun:
            print "\n".join( action.preview() )
        else:
            action.execute( self.keepGoing, self.jobs )
