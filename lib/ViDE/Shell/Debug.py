# Third-party libraries
import InteractiveCommandLine as icl

# Project
from CommandWithContext import CommandWithContext
from ViDE.Context import Context

class Debug(CommandWithContext):
    def __init__(self, program):
        CommandWithContext.__init__(self, program, "debug", "debug an executable file")

    def executeWithContext(self, context, *args):
        artifact = context.project.retrieveByName(args[0])
        if not hasattr(artifact, "debug"):
            artifact = context.project.retrieveByFile(context.fileName("bin", args[0]))
        artifact.debug(*args[1:])
