from ViDE.Project.Description import *

lib = CppDynamicLibrary(
    name = "lib",
    sources = [ "src/lib.cpp" ],
    headers = [ "src/lib.hpp", "src/lib/a.hpp", "src/lib/b.hpp", "src/lib/c.hpp" ],
    stripHeaders = lambda h: h[4:],
    localLibraries = [],
    externalLibraries = []
)

CppExecutable(
    name = "hello",
    sources = [ "main.cpp" ],
    localLibraries = [ lib ],
    externalLibraries = []
)
