from ViDE.Project.Description import *

a = CppHeaderLibrary(
    name = "a",
    headers = [ "a.hpp" ]
)

b = CppHeaderLibrary(
    name = "b",
    headers = [ "b.hpp" ],
    localLibraries = [ a ]
)

CppExecutable(
    name = "hello",
    sources = [ "main.cpp" ],
    localLibraries = [ b ]
)
