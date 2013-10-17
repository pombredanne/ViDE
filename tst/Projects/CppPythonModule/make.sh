#!/bin/sh

echo "Cleaning"
rm -rf build
mkdir -p build/obj/a/b
mkdir -p build/pyd/a/b
mkdir -p build/bin
mkdir -p build/tst

echo "Compiling"
g++ -c -o build/obj/a/b/c1.cpp.o a/b/c1.cpp $(python-config --includes) -fPIC || exit

cp a/b/c2.py build/pyd/a/b/c2.py
touch build/pyd/a/__init__.py build/pyd/a/b/__init__.py
python -m py_compile build/pyd/a/b/c2.py build/pyd/a/__init__.py build/pyd/a/b/__init__.py
rm build/pyd/a/b/c2.py build/pyd/a/__init__.py build/pyd/a/b/__init__.py

echo "Linking"
g++ -shared -o build/pyd/a/b/c1.so build/obj/a/b/c1.cpp.o -lboost_python $(python-config --libs) || exit

echo "Copying"
cp test.py build/bin/test
chmod +x build/bin/test

echo "Testing"
PYTHONPATH=build/pyd build/bin/test "Vincent" "Hello, Vincent!" && touch build/tst/test_Vincent.ok
PYTHONPATH=build/pyd build/bin/test "World" "Hello, World!" && touch build/tst/test_World.ok
