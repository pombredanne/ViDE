from ViDE.Project.Description import *
from Tools.Boost import BoostProgramOptions

CppExecutable(
    name = "hello",
    sources = [ "main.cpp" ],
    externalLibraries = [ BoostProgramOptions ]
)
