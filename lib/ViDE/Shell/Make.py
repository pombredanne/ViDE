from Misc import InteractiveCommandLineProgram as ICLP

from ViDE import Log
from ViDE.Core.Action import CompoundException
from ViDE.Core.ExecutionReport import ExecutionReport
from ViDE.Context import Context

class Make( ICLP.Command ):
    def __init__( self, program ):
        ICLP.Command.__init__( self, program )
        self.jobs = -1
        self.addOption( [ "j", "jobs" ], "jobs", ICLP.StoreArgument( "JOBS" ), "use JOBS parallel jobs" )
        self.keepGoing = False
        self.addOption( [ "k", "keep-going" ], "keepGoing", ICLP.StoreConstant( True ), "keep going in case of failure" )
        self.dryRun = False
        self.addOption( [ "n", "dry-run" ], "dryRun", ICLP.StoreConstant( True ), "print commands instead of executing them" )
        fakeAge = self.createOptionGroup( "Faking file age", "" )
        self.assumeNew = []
        fakeAge.addOption( [ "W", "what-if", "new-file", "assume-new" ], "assumeNew", ICLP.AppendArgument( "FILE" ), "assume that FILE is newer than its dependants" )
        self.assumeOld = []
        fakeAge.addOption( [ "o", "old-file", "assume-old" ], "assumeOld", ICLP.AppendArgument( "FILE" ), "assume that FILE is older than its dependants" )
        self.touch = False
        self.addOption( [ "t", "touch" ], "touch", ICLP.StoreConstant( True ), "touch targets instead of remaking them")
        ### @todo Add an option to build with all buildkits
        
    def execute( self, args ):
        context = Context( self.program )
        action = context.project.getBuildAction( assumeNew = self.assumeNew, assumeOld = self.assumeOld, touch = self.touch )
        # @todo project's include graph
        if self.dryRun:
            print "\n".join( action.preview() )
        else:
            try:
                action.execute( self.keepGoing, self.jobs )
            except CompoundException, e:
                Log.error( "build failed", e )
            finally:
                report = ExecutionReport( action, 800 )
                report.drawTo( context.fileName( "make-report.png" ) )
        action.getGraph().drawTo( context.fileName( "make-actions.png" ) )
        context.project.getGraph().drawTo( context.fileName( "make-artifacts.png" ) )
