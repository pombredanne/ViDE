from ViDE.Project.Description import *

lib = DynamicLibrary(
    name = "hello",
    headers = [ "lib.hpp" ],
    sources = [ "lib.cpp" ]
)

Executable(
    name = "hello",
    sources = [ "main.cpp" ],
    localLibraries = [ lib ]
)
