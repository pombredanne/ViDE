import unittest


class ParsingResult:
    def __init__(self, localIncludes, systemIncludes, conditions):
        self.localIncludes = localIncludes
        self.systemIncludes = systemIncludes
        self.conditions = conditions


def parseIncludesAndConditions(file):
    localIncludes = []
    systemIncludes = []
    conditions = []

    for line in file.split("\n"):
        line = line.strip()
        if line.startswith("#"):
            line = line[1:].lstrip()
            if line.startswith("include"):
                line = line[7:].strip()
                if line.startswith('"'):
                    localIncludes.append(line[1:-1])
                elif line.startswith('<'):
                    systemIncludes.append(line[1:-1])
            elif line.startswith("ifdef"):
                conditions.append(line[5:].lstrip())
            elif line.startswith("ifndef"):
                conditions.append(line[6:].lstrip())
            elif line.startswith("if"):
                i = line.find("defined")
                while i != -1:
                    line = line[i + 7:].lstrip()
                    if line.startswith("("):
                        line = line[1:]
                        j = line.find(")")
                        conditions.append(line[:j])
                        line = line[j:]
                    else:
                        j = line.find(" ")
                        if j == -1:
                            conditions.append(line)
                            line = ""
                        else:
                            conditions.append(line[:j])
                            line = line[j:]
                    i = line.find("defined")

    return ParsingResult(localIncludes, systemIncludes, conditions)


class BasicPreprocessorTestCase(unittest.TestCase):
    def testLocalInclude(self):
        self.assertEqual(parseIncludesAndConditions('#include "foo/bar.hpp"').localIncludes, ["foo/bar.hpp"])

    def testSystemIncludes(self):
        self.assertEqual(parseIncludesAndConditions('#include <foo/bar.hpp>').systemIncludes, ["foo/bar.hpp"])

    def testIfdef(self):
        self.assertEqual(parseIncludesAndConditions("#ifdef FOO").conditions, ["FOO"])

    def testIfndef(self):
        self.assertEqual(parseIncludesAndConditions("#ifndef FOO").conditions, ["FOO"])

    def testIfDefinedWithParenthesis(self):
        self.assertEqual(parseIncludesAndConditions("#if defined(FOO)").conditions, ["FOO"])

    def testIfDefinedWithoutParenthesisAtEndOfLine(self):
        self.assertEqual(parseIncludesAndConditions("#if defined FOO").conditions, ["FOO"])

    def testIfDefinedWithoutParenthesisBeforeEndOfLine(self):
        self.assertEqual(parseIncludesAndConditions("#if defined FOO || 1 == 3").conditions, ["FOO"])

    def testIfArbitraryExpression(self):
        self.assertEqual(parseIncludesAndConditions("#if 7 + FOO == 3").conditions, ["FOO"])


if __name__ == "__main__":
    unittest.main()
