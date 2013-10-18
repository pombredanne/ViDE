import InteractiveCommandLine as ICL

import ViDE.Project.ProjectDescription


class Check(ICL.Command):
    def __init__(self):
        ICL.Command.__init__(self, "check", "Run static code checks")

    def execute(self):
        # @todo Implement check with Actions and touch a file when checks pass (avoid checking unmodified files, include check in vide make)
        project = ViDE.Project.ProjectDescription.fromString(
            open("videfile.py").read()
        )
        project.check()
