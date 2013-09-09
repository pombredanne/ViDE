import InteractiveCommandLine as ICL

import Check


class Program(ICL.Program):
    def __init__(self):
        ICL.Program.__init__(self, "vide")
        self.addCommand(Check.Check())


def main():
    Program().execute()
