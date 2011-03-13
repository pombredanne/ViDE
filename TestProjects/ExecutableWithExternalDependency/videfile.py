from ViDE.Project.Description import *
from Tools.Cairo import Cairomm

CppExecutable(
    name = "hello",
    sources = [ "main.cpp" ],
    externalLibraries = [ Cairomm ]
)
