from ViDE.Project.Description import *

a = DynamicLibrary(
    name = "a",
    sources = [ "a.cpp" ],
    headers = [ "a.hpp", "a1.hpp", "a2.hpp" ]
)

b = DynamicLibrary(
    name = "b",
    sources = [ "b.cpp" ],
    headers = [ "b.hpp", "b1.hpp", "b2.hpp" ],
    localLibraries = [ a ]
)

Executable(
    name = "hello1",
    sources = [ "hello1.cpp" ],
    localLibraries = [ b ]
)

Executable(
    name = "hello2",
    sources = [ "hello2.cpp" ],
    localLibraries = [ b ]
)
