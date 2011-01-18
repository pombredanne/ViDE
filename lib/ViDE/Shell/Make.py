import os.path

import cairo

from Misc import InteractiveCommandLineProgram

from ViDE import Log
from ViDE.Core.Action import CompoundException
from ViDE.Core.ExecutionReport import ExecutionReport
from ViDE.Project.Project import Project

class Make( InteractiveCommandLineProgram.Command ):
    def __init__( self, program ):
        InteractiveCommandLineProgram.Command.__init__( self, program )
        self.jobs = -1
        self.addOption( [ "j", "jobs" ], "jobs", InteractiveCommandLineProgram.StoreArgument( "JOBS" ), "use JOBS parallel jobs" )
        self.keepGoing = False
        self.addOption( [ "k", "keep-going" ], "keepGoing", InteractiveCommandLineProgram.StoreConstant( True ), "keep going in case of failure" )
        self.dryRun = False
        self.addOption( [ "n", "dry-run" ], "dryRun", InteractiveCommandLineProgram.StoreConstant( True ), "print commands instead of executing them" )
        self.drawGraph = False
        self.addOption( [ "draw-graph" ], "drawGraph", InteractiveCommandLineProgram.StoreConstant( True ), "print the dot graph of the commands instead of executing them" )
        
    def execute( self, args ):
        action = Project.load( "videfile.py" ).getBuildAction()
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
            report = ExecutionReport( action )
            img = cairo.ImageSurface( cairo.FORMAT_RGB24, 800, 600 )
            ctx = cairo.Context( img )
            ctx.translate( 10, 10 )
            ctx.set_source_rgb( .9, .9, .9 )
            ctx.paint()
            report.draw( ctx, 780, 580 )
            img.write_to_png( os.path.join( "build", "report.png" ) )
