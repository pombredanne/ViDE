import cairo

from Misc import InteractiveCommandLineProgram as ICLP

import ViDE
from ViDE import Log
from ViDE.Core.Action import CompoundException
from ViDE.Core.ExecutionReport import ExecutionReport
from ViDE.Project.Project import Project
from ViDE.Buildkit import Buildkit
from ViDE.Toolset import Toolset

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
        buildkit = Buildkit.load( self.program.buildkit, self.program.flavour )
        toolset = Toolset.load( self.program.toolset )
        project = Project.load( buildkit, toolset )
        action = project.getBuildAction( assumeNew = self.assumeNew, assumeOld = self.assumeOld, touch = self.touch )
        # @todo project's include/import graph
        if self.dryRun:
            print "\n".join( action.preview() )
        else:
            try:
                action.execute( self.keepGoing, self.jobs )
            except CompoundException, e:
                Log.error( "build failed", e )
            finally:
                report = ExecutionReport( action, 800 )
                report.drawTo( buildkit.fileName( "make-report.png" ) )
        action.getGraph().drawTo( buildkit.fileName( "make-actions.png" ) )
        project.getGraph().drawTo( buildkit.fileName( "make-artifacts.png" ) )
