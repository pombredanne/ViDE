import Python
import Cpp


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


def PythonScript(source):
    return Python.Script(PythonSource(source))


def PythonModule(source, strip=identity):
    return Python.Module(PythonSource(source), strip)


def CppPythonModule(name, sources=[], objects=[],
                    localLibraries=[], externalLibraries=[]):
    return Python.CppModule(name, [CppObjectFile(CppSource(s)) for s in sources] + objects)


def PythonPackage(name, sources=[], modules=[], strip=identity):
    return Python.Package(
        name,
        [PythonModule(s, strip) for s in sources] + modules
    )


allFactories = [
    PythonSource,
    PythonModule,
    PythonPackage,
    PythonScript,
    CppPythonModule,
    CppSource,
    CppObjectFile,
]
