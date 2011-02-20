from ViDE.Project.Description import *

lib = CppStaticLibrary(
    name = "hello",
    headers = [ "src/lib.hpp", "src/sub/sub.hpp" ],
    sources = [ "src/lib.cpp" ],
    stripHeaders = lambda f: f[4:]
)

CppExecutable(
    name = "hello",
    sources = [ "main.cpp" ],
    localLibraries = [ lib ]
)
