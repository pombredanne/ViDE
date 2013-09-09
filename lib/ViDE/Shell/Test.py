import subprocess

import InteractiveCommandLine as ICL


class Test(ICL.Command):
    def __init__(self):
        ICL.Command.__init__(self, "test", "Run tests")

    def execute(self):
        subprocess.check_call(["coverage", "run", "--omit", "setup.py,*/tests/*.py", "--branch", "setup.py", "test", "--quiet"])
        subprocess.check_call(["coverage", "report", "--show-missing"])
        subprocess.check_call(["python3", "setup.py", "test", "--quiet"])
