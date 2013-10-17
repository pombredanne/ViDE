import Python
import Cpp
import Testing


identity = lambda s: s


def CppSource(source):
    if isinstance(source, (str, unicode)):
        return Cpp.Source(source)
    else:
        return source


def CppObjectFile(source):
    return Cpp.ObjectFile(CppSource(source))


def PythonSource(source):
    if isinstance(source, (str, unicode)):
        return Python.Source(source)
    else:
        return source


def PythonScript(source, packages=[]):
    # @todo packages could contain strings (a.py) and PythonSources that should be transformed in PythonModules
    return Python.Script(PythonSource(source), packages)


def PythonModule(source, strip=identity):
    return Python.Module(PythonSource(source), strip)


def CppPythonModule(name, sources=[], objects=[],
                    localLibraries=[], externalLibraries=[]):
    return Python.CppModule(name, [CppObjectFile(CppSource(s)) for s in sources] + objects)


def PythonPackage(name, sources=[], packages=[], strip=identity):
    return Python.Package(
        name,
        [PythonModule(s, strip) for s in sources] + packages
    )


allFactories = [
    CppSource,
    CppObjectFile,
    PythonSource,
    PythonModule,
    PythonPackage,
    PythonScript,
    CppPythonModule,
    Testing.UnitTest,
]
