from ViDE.Project.Description import *

lib = CppStaticLibrary(
    name = "hello",
    headers = [ "lib.hpp" ],
    sources = [ "lib.cpp" ]
)

CppExecutable(
    name = "hello",
    sources = [ "main.cpp" ],
    localLibraries = [ lib ]
)
