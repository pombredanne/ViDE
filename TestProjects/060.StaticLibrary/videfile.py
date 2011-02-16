from ViDE.Project.Description import *

lib = StaticLibrary(
    name = "hello",
    headers = [ "lib.hpp" ],
    sources = [ "lib.cpp" ]
)

Executable(
    name = "hello",
    sources = [ "main.cpp" ],
    localLibraries = [ lib ]
)
