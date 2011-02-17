from ViDE.Project.Description import *

a = DynamicLibrary(
    name = "a",
    sources = [ "a.cpp" ],
    headers = [ "a.hpp" ]
)

b = HeaderLibrary(
    name = "b",
    headers = [ "b.hpp" ],
    localLibraries = [ a ]
)

Executable(
    name = "hello",
    sources = [ "main.cpp" ],
    localLibraries = [ b ]
)
