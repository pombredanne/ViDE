import cairo

from Misc import InteractiveCommandLineProgram as ICLP

import ViDE
from ViDE import Log
from ViDE.Core.Action import CompoundException
from ViDE.Core.ExecutionReport import ExecutionReport
from ViDE.Toolset import Toolset

class InstallTools( ICLP.Command ):
    def __init__( self, program ):
        ICLP.Command.__init__( self, program )
        self.jobs = 1
        self.addOption( [ "j", "jobs" ], "jobs", ICLP.StoreArgument( "JOBS" ), "use JOBS parallel jobs" )
        self.keepGoing = False
        self.addOption( [ "k", "keep-going" ], "keepGoing", ICLP.StoreConstant( True ), "keep going in case of failure" )
        self.dryRun = False
        self.addOption( [ "n", "dry-run" ], "dryRun", ICLP.StoreConstant( True ), "print commands instead of executing them" )
        
    def execute( self, args ):
        toolset = Toolset.load( self.program.toolset )
        action = toolset.getFetchArtifact().getProductionAction()
        if self.dryRun:
            print "\n".join( action.preview() )
        else:
            try:
                action.execute( self.keepGoing, self.jobs )
            except CompoundException, e:
                Log.error( "installation failed", e )
            finally:
                report = ExecutionReport( action, 800 )
                #report.drawTo( toolset.fileName( "installation-report.png" ) )
                report.drawTo( "installation-report.png" )
