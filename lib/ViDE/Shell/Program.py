import InteractiveCommandLine as ICL

import Check
import Test


class Program(ICL.Program):
    def __init__(self):
        ICL.Program.__init__(self, "vide")
        self.addCommand(Check.Check())
        self.addCommand(Test.Test())
