import imp
import os.path

import cairo

from Misc import InteractiveCommandLineProgram as ICLP

import ViDE
from ViDE import Log
from ViDE.Core.Action import CompoundException
from ViDE.Core.ExecutionReport import ExecutionReport
from ViDE.Project.Project import Project
from ViDE.BuildKit.BuildKit import BuildKit

class Make( ICLP.Command ):
    def __init__( self, program ):
        ICLP.Command.__init__( self, program )
        self.jobs = -1
        self.addOption( [ "j", "jobs" ], "jobs", ICLP.StoreArgument( "JOBS" ), "use JOBS parallel jobs" )
        self.keepGoing = False
        self.addOption( [ "k", "keep-going" ], "keepGoing", ICLP.StoreConstant( True ), "keep going in case of failure" )
        self.dryRun = False
        self.addOption( [ "n", "dry-run" ], "dryRun", ICLP.StoreConstant( True ), "print commands instead of executing them" )
        self.drawGraph = False
        self.addOption( [ "draw-graph" ], "drawGraph", ICLP.StoreConstant( True ), "print the dot graph of the commands instead of executing them" )
        
    def execute( self, args ):
        buildKit = imp.load_source( self.program.buildkit, os.path.join( ViDE.buildKitsDirectory, self.program.buildkit + ".py" ) )
        #buildKit = BuildKit.load( os.path.join( ViDE.buildKitsDirectory, self.program.buildkit + ".py" ) )
        action = Project.load( "videfile.py", buildKit ).getBuildAction()
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
            ### @todo Draw the ExecutionReport even in case of build failure
            report = ExecutionReport( action )
            img = cairo.ImageSurface( cairo.FORMAT_RGB24, 800, 600 )
            ctx = cairo.Context( img )
            ctx.translate( 10, 10 )
            ctx.set_source_rgb( .9, .9, .9 )
            ctx.paint()
            report.draw( ctx, 780, 580 )
            img.write_to_png( os.path.join( "build", "report.png" ) ) ### @todo Put the ExecutionReport in the right folder
