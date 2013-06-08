# Third-party libraries
import InteractiveCommandLine as icl

# Project
from CommandWithContext import CommandWithContext
from ViDE.Context import Context


### @todo Merge with commands 'debug' and 'valgrind', by adding options
class Run(CommandWithContext):
    def __init__(self, program):
        CommandWithContext.__init__(self, program, "run", "run an executable file")

    def executeWithContext(self, context, *args):
        artifact = context.project.retrieveByName(args[0])
        if not hasattr(artifact, "run"):
            artifact = context.project.retrieveByFile(context.fileName("bin", args[0]))
        artifact.run(*args[1:])
