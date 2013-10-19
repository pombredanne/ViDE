import cairo
import InteractiveCommandLine as ICL
import ActionTree.Drawings

import ViDE.Project.ProjectDescription


class Build(ICL.Command):
    def __init__(self):
        ICL.Command.__init__(
            self, "build", "Build the artifacts of the project"
        )
        self.touch = False
        self.addOption(ICL.StoringOption("touch", "Instead of building the artifacts, just touch them", self, "touch", ICL.ConstantValue(True)))
        self.preview = False
        self.addOption(ICL.StoringOption("preview", "Display the commands that would be run", self, "preview", ICL.ConstantValue(True)))

    def execute(self):
        project = ViDE.Project.ProjectDescription.fromString(
            open("videfile.py").read()
        )
        if self.touch:
            action = project.getTouchAction([], [])
        else:
            action = project.getBuildAction([], [])
        ActionTree.Drawings.ActionGraph(action).drawTo("action.png")
        if self.preview:
            print "\n".join(a for a in action.getPreview() if a != "nop")
        else:
            action.execute()
            r = ActionTree.Drawings.ExecutionReport(action)
            w = 800
            ctx = cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 1, 1))
            h = r.getHeight(ctx)
            img = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
            ctx = cairo.Context(img)
            ctx.set_source_rgb(1, 1, 1)
            ctx.paint()
            r.draw(ctx, w)
            img.write_to_png("build.png")
