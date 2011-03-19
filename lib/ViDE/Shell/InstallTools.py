from Misc import InteractiveCommandLineProgram as ICLP

from ViDE import Log
from ViDE.Core.Action import CompoundException
from ViDE.Core.ExecutionReport import ExecutionReport
from ViDE.Context import Context

class InstallTools( ICLP.Command ):
    def __init__( self, program ):
        ICLP.Command.__init__( self, program )
        self.jobs = 1
        self.addOption( [ "j", "jobs" ], "jobs", ICLP.StoreArgument( "JOBS" ), "use JOBS parallel jobs" )
        self.keepGoing = False
        self.addOption( [ "k", "keep-going" ], "keepGoing", ICLP.StoreConstant( True ), "keep going in case of failure" )
        self.dryRun = False
        self.addOption( [ "n", "dry-run" ], "dryRun", ICLP.StoreConstant( True ), "print commands instead of executing them" )
        self.downloadOnly = False
        self.addOption( [ "d", "dl-only" ], "downloadOnly", ICLP.StoreConstant( True ), "only do the part of installation which needs internet access" )
        
    def execute( self, args ):
        context = Context( self.program )
        if self.downloadOnly:
            artifact = context.toolset.getFetchArtifact()
        else:
            artifact = context.toolset.getInstallArtifact()
        action = artifact.getProductionAction()
        if self.dryRun:
            print "\n".join( action.preview() )
        else:
            try:
                action.execute( self.keepGoing, self.jobs )
            except CompoundException, e:
                Log.error( "installation failed", e )
            finally:
                report = ExecutionReport( action, 800 )
                report.drawTo( "installation-report.png" )
        artifact.getGraph().drawTo( "installation-artifacts.png" )
        action.getGraph().drawTo( "installation-actions.png" )
