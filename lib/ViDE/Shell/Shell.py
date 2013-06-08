# Third party libraries
import InteractiveCommandLine as icl

# Project
from ViDE import Log
from ViDE.Shell.Make import Make
from ViDE.Shell.Run import Run
from ViDE.Shell.Debug import Debug

class Shell(icl.Program):
    def __init__(self):
        icl.Program.__init__(self, "vide", invite="ViDE>")

        verbosity = self.createOptionGroup("Verbosity")
        verbosity.addOption(icl.StoringOption("silent", "print absolutely nothing (not even error messages)", Log, "level", icl.ConstantValue(-1), icl.ConstantValue(1)))
        verbosity.addOption(icl.StoringOption("quiet", "print as few messages as possible", Log, "level", icl.ConstantValue(0), icl.ConstantValue(1)))
        verbosity.addOption(icl.StoringOption("verbose", "print more information messages", Log, "level", icl.ConstantValue(2), icl.ConstantValue(1)))
        verbosity.addOption(icl.StoringOption("debug", "print debug messages", Log, "level", icl.ConstantValue(3), icl.ConstantValue(1)))

        generation = self.createCommandGroup("Artifact generation")
        generation.addCommand(Make(self))
        
        running = self.createCommandGroup("Executable artifact running")
        running.addCommand(Run(self))
        running.addCommand(Debug(self))
