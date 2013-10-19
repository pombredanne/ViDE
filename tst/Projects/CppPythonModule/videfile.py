Project(
    name="Project name"
)

abc1 = CppPythonModule(
    name="a.b.c1",
    sources=["a/b/c1.cpp"]
)

abc2 = PythonModule(
    source="a/b/c2.py"
)

ab = PythonPackage(
    name="a.b",
    sources=["a/b/__init__.py"],
    packages=[abc1, abc2]
)

a = PythonPackage(
    name="a",
    sources=["a/__init__.py"],
    packages=[ab]
)

test = PythonScript("test.py", packages=[a])

UnitTest(test, "World", "Hello, World!")
UnitTest(test, "Vincent", "Hello, Vincent!")
