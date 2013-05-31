# Third-party libraries
import ActionTree.Drawings
from ActionTree import CompoundException
import InteractiveCommandLine as icl

# Project
from ViDE import Log
from ViDE.Context import Context
from CommandWithContext import CommandWithContext

class Make(CommandWithContext):
    def __init__(self, program):
        CommandWithContext.__init__(self, program, "make", "build the project")
        self.jobs = -1
        self.addOption(icl.StoringOption("jobs", "use JOBS parallel jobs", self, "jobs", icl.ValueFromOneArgument("JOBS", int)))
        self.keepGoing = False
        self.addOption(icl.StoringOption("keep-going", "keep going in case of failure", self, "keepGoing", icl.ConstantValue(True)))
        self.dryRun = False
        self.addOption(icl.StoringOption("dry-run", "print commands instead of executing them", self, "dryRun", icl.ConstantValue(True)))
        fakeAge = self.createOptionGroup("Faking file age")
        self.assumeNew = []
        fakeAge.addOption(icl.AppendingOption("assume-new", "assume that FILE is newer than its dependants", self.assumeNew, icl.ValueFromOneArgument("FILE")))
        self.assumeOld = []
        fakeAge.addOption(icl.AppendingOption("assume-old", "assume that FILE is older than its dependants", self.assumeOld, icl.ValueFromOneArgument("FILE")))
        self.touch = False
        self.addOption(icl.StoringOption("touch", "touch targets instead of remaking them", self, "touch", icl.ConstantValue(True)))
        ### @todo Add an option to build with all buildkits
        
    def executeWithContext(self, context):
        action = context.project.getBuildAction(assumeNew=self.assumeNew, assumeOld=self.assumeOld, touch=self.touch)
        # @todo project's include graph
        if self.dryRun:
            print "\n".join(action.getPreview())
        else:
            try:
                action.execute(self.jobs, self.keepGoing)
            except CompoundException, e:
                Log.error( "build failed", e )
            finally:
                report = ActionTree.Drawings.ExecutionReport( action )
                # report.drawTo( context.fileName( "make-report.png" ), 800 )
        ActionTree.Drawings.ActionGraph(action).drawTo( context.fileName( "make-actions.png" ) )
        context.project.getGraph().drawTo( context.fileName( "make-artifacts.png" ) )
