from ViDE.Project.Description import *

a = CppHeaderLibrary(
    name = "a",
    headers = [ "a.hpp" ]
)

b = CppStaticLibrary(
    name = "b",
    sources = [ "b.cpp" ],
    headers = [ "b.hpp" ],
    localLibraries = [ a ]
)

CppExecutable(
    name = "hello",
    sources = [ "main.cpp" ],
    localLibraries = [ b ]
)
