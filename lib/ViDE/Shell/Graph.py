import InteractiveCommandLine as ICL

import ViDE.Project.ProjectDescription


class Graph(ICL.Command):
    def __init__(self):
        ICL.Command.__init__(
            self, "graph", "Draw the graph of the artifacts of the project"
        )

    def execute(self):
        project = ViDE.Project.ProjectDescription.fromString(
            open("videfile.py").read()
        )
        project.getGraph().drawTo("project.png")
