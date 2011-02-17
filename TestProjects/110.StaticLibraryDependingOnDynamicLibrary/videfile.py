from ViDE.Project.Description import *

a = DynamicLibrary(
    name = "a",
    sources = [ "a.cpp" ],
    headers = [ "a.hpp" ]
)

b = StaticLibrary(
    name = "b",
    sources = [ "b.cpp" ],
    headers = [ "b.hpp" ],
    localLibraries = [ a ]
)

Executable(
    name = "hello",
    sources = [ "main.cpp" ],
    localLibraries = [ b ]
)
