from ViDE.Project.Description import *

lib = HeaderLibrary(
    name = "hello",
    headers = [ "lib.hpp" ]
)

Executable(
    name = "hello",
    sources = [ "main.cpp" ],
    localLibraries = [ lib ]
)
