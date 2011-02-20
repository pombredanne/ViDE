from ViDE.Project.Description import *

a = CppDynamicLibrary(
    name = "a",
    sources = [ "a.cpp" ],
    headers = [ "a.hpp" ]
)

b = CppStaticLibrary(
    name = "b",
    sources = [ "b.cpp" ],
    headers = [ "b.hpp" ],
    localLibraries = [ a ]
)

CppExecutable(
    name = "hello",
    sources = [ "main.cpp" ],
    localLibraries = [ b ]
)
