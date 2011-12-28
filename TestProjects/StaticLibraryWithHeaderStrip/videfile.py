from ViDE.Project.Description import *

lib = CppStaticLibrary(
    name = "hello",
    headers = [ os.path.join( "src", "lib.hpp" ), os.path.join( "src", "sub", "sub.hpp" ) ],
    sources = [ os.path.join( "src", "lib.cpp" ) ],
    stripHeaders = lambda f: f[4:]
)

CppExecutable(
    name = "hello",
    sources = [ "main.cpp" ],
    localLibraries = [ lib ]
)
