from ViDE.Project.Description import *

a = CppStaticLibrary(
    name = "a",
    sources = [ "a.cpp" ],
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
