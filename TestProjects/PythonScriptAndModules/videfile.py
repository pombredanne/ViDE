from ViDE.Project.Description import *

PythonModule(
    source = "a.py"
)

b1 = PythonModule(
    source = "pack/b/b1.py",
    strip = lambda f: f[5:]
)

PythonPackage(
    name = "b",
    sources = [ PythonSource( "pack/b/__init__.py" ), "pack/b/b2.py" ],
    modules = [ b1 ],
    strip = lambda f: f[5:]
)

PythonScript(
    source = "hello.py"
)
