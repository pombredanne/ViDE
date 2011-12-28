from ViDE.Project.Description import *

lib = CppDynamicLibrary(
    name = "lib",
    sources = [ os.path.join( "src", "lib.cpp" ) ],
    headers = [ os.path.join( "src", "lib.hpp" ), os.path.join( "src", "lib", "a.hpp" ), os.path.join( "src", "lib", "b.hpp" ), os.path.join( "src", "lib", "c.hpp" ) ],
    stripHeaders = lambda h: h[4:],
    localLibraries = [],
    externalLibraries = []
)

CppExecutable(
    name = "hello",
    sources = [ "main.cpp" ],
    localLibraries = [ lib ],
    externalLibraries = []
)
