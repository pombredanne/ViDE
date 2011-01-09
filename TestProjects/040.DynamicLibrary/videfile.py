from ViDE.Project.Description import *

lib = DynamicLibrary(
    name = "hello",
    sources = [ "lib.cpp" ]
)

Executable(
    name = "hello",
    sources = [ "main.cpp" ],
    localLibraries = [ lib ]
)
