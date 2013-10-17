Project(
    name="Project name"
)

ab1c1 = CppPythonModule(
    name="a.b1.c1",
    sources=["a/b1/c1.cpp"]
)

ab1c2 = PythonModule(
    source="a/b1/c2.py"
)

ab1 = PythonPackage(
    name="a.b1",
    modules=[ab1c1, ab1c2]
)

a = PythonPackage(
    name="a",
    modules=[ab1]
)
