import unittest
import itertools


def transformGraph(root, children, transform):
    transformed = {}

    def goDeeper(node):
        nodeChildren = children(node)
        for child in itertools.chain.from_iterable(nodeChildren.itervalues()):
            goDeeper(child)
        if id(node) not in transformed:
            transformedChildren = {}
            for category, childs in nodeChildren.iteritems():
                transformedChildren[category] = [
                    transformed[id(child)]
                    for child in childs
                ]
            transformed[id(node)] = transform(node, transformedChildren)

    goDeeper(root)

    return transformed[id(root)]


class TestCase(unittest.TestCase):
    def testTreeStructure(self):
        g = ("A", [
            ("AA", [
                ("AAA", []),
                ("AAB", [])
            ]),
            ("AB", [
                ("ABA", []),
                ("ABB", [])
            ])
        ])

        h = transformGraph(
            g,
            lambda n: {"children": n[1]},
            lambda n, children: (n[0].lower(), children["children"])
        )

        self.assertEqual(
            h,
            ("a", [
                ("aa", [
                    ("aaa", []),
                    ("aab", []),
                ]),
                ("ab", [
                    ("aba", []),
                    ("abb", []),
                ]),
            ])
        )

    def testDiamondStructure(self):
        s = ("S", [])
        g = ("A", [
            ("AA", [s]),
            ("AB", [s])
        ])

        h = transformGraph(
            g,
            lambda n: {"children": n[1]},
            lambda n, children: (n[0].lower(), children["children"])
        )

        self.assertEqual(
            h,
            ("a", [
                ("aa", [
                    ("s", [])
                ]),
                ("ab", [
                    ("s", [])
                ]),
            ])
        )

        self.assertIs(h[1][0][1][0], h[1][1][1][0])

if __name__ == "__main__":
    unittest.main()
