from ViDE.Project.Description import *

a = CppDynamicLibrary(
    name = "a",
    sources = [ "a.cpp" ],
    headers = [ "a.hpp", "a1.hpp", "a2.hpp" ]
)

b = CppDynamicLibrary(
    name = "b",
    sources = [ "b.cpp" ],
    headers = [ "b.hpp", "b1.hpp", "b2.hpp" ],
    localLibraries = [ a ]
)

CppExecutable(
    name = "hello1",
    sources = [ "hello1.cpp" ],
    localLibraries = [ b ]
)

CppExecutable(
    name = "hello2",
    sources = [ "hello2.cpp" ],
    localLibraries = [ b ]
)

h = CppHeaderLibrary(
    name = "h",
    headers = [ "H/h1.hpp", "H/h2.hpp" ]
)

CppExecutable(
    name = "hello3",
    sources = [ "hello3.cpp" ],
    localLibraries = [ h ]
)

CppExecutable(
    name = "hello4",
    sources = [ "hello4.cpp" ],
    localLibraries = []
)
