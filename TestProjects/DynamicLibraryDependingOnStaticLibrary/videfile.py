from ViDE.Project.Description import *

a = StaticLibrary(
    name = "a",
    sources = [ "a.cpp" ],
    headers = [ "a.hpp" ]
)

b = DynamicLibrary(
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
