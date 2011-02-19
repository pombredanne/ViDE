import cairo

from Misc import InteractiveCommandLineProgram as ICLP

import ViDE
from ViDE import Log
from ViDE.Core.Action import CompoundException
from ViDE.Core.ExecutionReport import ExecutionReport
from ViDE.Project.Project import Project
from ViDE.Buildkit import Buildkit

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
        ### @todo Always draw the graph of actions, near report.png. Remove this drawGraph option
        self.drawGraph = False
        self.addOption( [ "draw-graph" ], "drawGraph", ICLP.StoreConstant( True ), "print the dot graph of the commands instead of executing them" )
        ### @todo Add an option to build with all buildkits
        
    def execute( self, args ):
        buildkit = Buildkit.load( self.program.buildkit )
        project = Project.load( buildkit )
        action = project.getBuildAction( assumeNew = self.assumeNew, assumeOld = self.assumeOld )
        if self.dryRun:
            print "\n".join( action.preview() )
        elif self.drawGraph:
            print action.getGraph().dotString()
        else:
            try:
                action.execute( self.keepGoing, self.jobs )
            except CompoundException, e:
                Log.error( "build failed", e )
                raise
            finally:
                # @todo Fix ExecutionReport when no action has been executed (vide make; vide make)
                report = ExecutionReport( action )
                img = cairo.ImageSurface( cairo.FORMAT_RGB24, 800, 600 )
                ctx = cairo.Context( img )
                ctx.translate( 10, 10 )
                ctx.set_source_rgb( .9, .9, .9 )
                ctx.paint()
                report.draw( ctx, 780, 580 )
                img.write_to_png( buildkit.fileName( "report.png" ) )
