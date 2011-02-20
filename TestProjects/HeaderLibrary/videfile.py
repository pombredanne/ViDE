from ViDE.Project.Description import *

lib = CppHeaderLibrary(
    name = "hello",
    headers = [ "lib.hpp" ]
)

CppExecutable(
    name = "hello",
    sources = [ "main.cpp" ],
    localLibraries = [ lib ]
)
