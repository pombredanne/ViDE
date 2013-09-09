import subprocess

import InteractiveCommandLine as ICL


class Check(ICL.Command):
    def __init__(self):
        ICL.Command.__init__(self, "check", "Run static code checks")

    def execute(self):
        subprocess.check_call(["pep8", "."])
        # Call pylint, and other static code analysis programs based on languages in project
