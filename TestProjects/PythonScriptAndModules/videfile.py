from ViDE.Project.Description import *

PythonModule(
    source = "a.py"
)

b1 = PythonModule(
    source = "pack/b/b1.py",
    strip = lambda f: f[5:]
)

b3 = CppPythonModule(
    name = "b.b3",
    sources = [ "b3.cpp" ],
    localLibraries = []
)

PythonPackage(
    name = "b",
    sources = [ PythonSource( "pack/b/__init__.py" ), "pack/b/b2.py" ],
    modules = [ b1, b3 ],
    strip = lambda f: f[5:]
)

PythonScript(
    source = "hello.py"
)
