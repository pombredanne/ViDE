# -*- coding: utf-8 -*-

import unittest


class EvalExecTestCase(unittest.TestCase):
    def testEvalIsLimitedToExpressions(self):
        self.assertEqual(eval("40 + 2"), 42)

    def testExecPolutesDir(self):
        self.assertNotIn("a", dir())
        exec "import os\na=42"
        self.assertIn("a", dir())
        self.assertIn("os", dir())

    def testExecInCustomDict(self):
        d = {"f": lambda x: 2 * x}
        exec "import os\na=f(21)" in d
        self.assertNotIn("a", dir())
        self.assertNotIn("os", dir())
        self.assertIn("a", d)
        self.assertEqual(d["a"], 42)
        self.assertIn("os", d)

unittest.main()
