from ViDE.Project.Description import *

main = CppObject( "main.cpp" )

sub = FortranObject( "sub.for" )

Executable(
    name = "hello",
    objects = [ main, sub ]
)
