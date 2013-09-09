import Python

identity = lambda s: s


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
    return Python.CModule()


def PythonPackage(name, sources=[], modules=[], strip=identity):
    return Python.Package(
        name,
        [PythonModule(source, strip) for source in sources] + modules
    )


allFactories = [
    PythonSource,
    PythonModule,
    PythonPackage,
    PythonScript,
    CppPythonModule,
]
