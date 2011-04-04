from ViDE.Project.Description import *

lib = CppDynamicLibrary(
    name = "lib",
    sources = [ "src/lib.cpp" ],
    headers = [ "src/lib/a.hpp", "src/lib/b.hpp", "src/lib.hpp" ],
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
