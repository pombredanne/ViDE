#!/usr/bin/env python

import sys

import a.b.c1
import a.b.c2

name = sys.argv[1]
expected = sys.argv[2]

assert a.b.c1.foo(name) == expected
assert a.b.c2.foo(name) == expected
