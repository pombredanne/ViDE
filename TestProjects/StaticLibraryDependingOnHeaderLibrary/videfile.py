from ViDE.Project.Description import *

a = HeaderLibrary(
    name = "a",
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
