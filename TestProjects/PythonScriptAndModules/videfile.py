from ViDE.Project.Description import *

PythonModule(
    source = "a.py"
)

PythonPackage(
    name = "b",
    sources = [ "pack/b/__init__.py", "pack/b/b1.py", "pack/b/b2.py" ],
    strip = lambda f: f[5:]
)

PythonScript(
    source = "hello.py"
)
