import unittest

from Graphviz import *

class GlobalTest( unittest.TestCase ):
    def test( self ):
        Node.nextId = 0
        Cluster.nextId = 0
        g = Graph( "First graph" )
        g.nodeAttr[ "shape" ] = "box"
        g.edgeAttr[ "color" ] = "red"
        n1 = Node( "Blue node" )
        n1.attr[ "color" ] = "blue"
        g.add( n1 )
        n2 = Node( "Second node" )
        g.add( n2 )
        c1 = Cluster( "First cluster" )
        g.add( c1 )
        n3 = Node( "Oval node" )
        n3.attr[ "shape" ] = "oval"
        c1.add( n3 )
        c2 = Cluster( "Second cluster" )
        g.add( c2 )
        n4 = Node( "Fourth node" )
        c2.add( n4 )

        g.add( Link( n1, n2 ) ) # First link, unnamed
        g.add( Link( n1, n3, "Second link" ) )
        l = Link( n2, c1, "Green link from node to cluster" )
        l.attr[ "color" ] = "green"
        g.add( l )
        g.add( Link( c1, n4, "Link from cluster to node" ) )
        g.add( Link( c1, c2, "Link between clusters" ) )

        self.assertEquals( g.dotString(), """digraph "First graph" {compound="true";node [shape="box"];edge [color="red"];node_0[color="blue",label="Blue node"];node_1[label="Second node"];subgraph cluster_0{label="First cluster";node_2[label="Oval node",shape="oval"];};subgraph cluster_1{label="Second cluster";node_3[label="Fourth node"];};node_0->node_1[];node_0->node_2[label="Second link"];node_1->node_2[color="green",label="Green link from node to cluster",lhead="cluster_0"];node_2->node_3[label="Link between clusters",lhead="cluster_1",ltail="cluster_0"];node_2->node_3[label="Link from cluster to node",ltail="cluster_0"];}""" )

class EqualityTestCase:
    def test( self ):
        g1 = self.createGraph()
        g2 = self.createGraph()
        self.assertTrue( Graph.areSame( g1, g2 ) )
        self.assertTrue( Graph.areSame( g2, g1 ) )

class EmptyEquality( unittest.TestCase, EqualityTestCase ):
    def createGraph( self ):
        return Graph( "Empty" )

class NodesAndLinksEquality( unittest.TestCase, EqualityTestCase ):
    def createGraph( self ):
        g = Graph( "Nodes and links" )
        n1 = Node( "Node 1" )
        g.add( n1 )
        n2 = Node( "Node 2" )
        g.add( n2 )
        n3 = Node( "Node 3" )
        g.add( n3 )
        g.add( Link( n1, n2, "Link 1" ) )
        g.add( Link( n2, n3, "Link 2" ) )
        return g

class ClusterLinkEquality( unittest.TestCase, EqualityTestCase ):
    def createGraph( self ):
        g = Graph( "Nodes and clusters" )
        n11 = Node( "Node 11" )
        n12 = Node( "Node 12" )
        n13 = Node( "Node 13" )
        c1 = Cluster( "Cluster 1" )
        c1.add( n11 )
        c1.add( n12 )
        c1.add( n13 )
        n21 = Node( "Node 21" )
        n22 = Node( "Node 22" )
        n23 = Node( "Node 23" )
        c2 = Cluster( "Cluster 2" )
        c2.add( n21 )
        c2.add( n22 )
        c2.add( n23 )
        g.add( c1 )
        g.add( c2 )
        g.add( Link( c1, c2, "Link" ) )
        return g

class ReccursiveClustersEquality( unittest.TestCase, EqualityTestCase ):
    def createGraph( self ):
        n111 = Node( "Node 111" )
        n112 = Node( "Node 112" )
        c11 = Cluster( "Cluster 11" )
        c11.add( n111 )
        c11.add( n112 )
        n121 = Node( "Node 121" )
        n122 = Node( "Node 122" )
        c12 = Cluster( "Cluster 12" )
        c12.add( n121 )
        c12.add( n122 )
        c1 = Cluster( "Cluster 1" )
        c1.add( c11 )
        c1.add( c12 )

        n211 = Node( "Node 211" )
        n212 = Node( "Node 212" )
        c21 = Cluster( "Cluster 21" )
        c21.add( n211 )
        c21.add( n212 )
        n221 = Node( "Node 221" )
        n222 = Node( "Node 222" )
        c22 = Cluster( "Cluster 22" )
        c22.add( n221 )
        c22.add( n222 )
        c2 = Cluster( "Cluster 2" )
        c2.add( c21 )
        c2.add( c22 )

        g = Graph( "Nodes and clusters" )
        g.add( c1 )
        g.add( c2 )

        g.add( Link( n111, n222, "Link" ) )
        return g

class DifferenceTestCase:
    def test( self ):
        g1 = self.createGraph1()
        g2 = self.createGraph2()
        self.assertFalse( Graph.areSame( g1, g2 ) )
        self.assertFalse( Graph.areSame( g2, g1 ) )

class OneMoreLinkDifference( unittest.TestCase, DifferenceTestCase ):
    def createGraph1( self ):
        g, n2, n3 = self.createBasicGraph()
        return g

    def createGraph2( self ):
        g, n2, n3 = self.createBasicGraph()
        g.add( Link( n2, n3, "Link 2" ) )
        return g

    def createBasicGraph( self ):
        g = Graph( "Nodes and links" )
        n1 = Node( "Node 1" )
        g.add( n1 )
        n2 = Node( "Node 2" )
        g.add( n2 )
        n3 = Node( "Node 3" )
        g.add( n3 )
        g.add( Link( n1, n2, "Link 1" ) )
        return g, n2, n3

class LinkNameDifference( unittest.TestCase, DifferenceTestCase ):
    def createGraph1( self ):
        g, n2, n3 = self.createBasicGraph()
        g.add( Link( n2, n3, "Link 2" ) )
        return g

    def createGraph2( self ):
        g, n2, n3 = self.createBasicGraph()
        g.add( Link( n2, n3, "Link 2 bis" ) )
        return g

    def createBasicGraph( self ):
        g = Graph( "Nodes and links" )
        n1 = Node( "Node 1" )
        g.add( n1 )
        n2 = Node( "Node 2" )
        g.add( n2 )
        n3 = Node( "Node 3" )
        g.add( n3 )
        g.add( Link( n1, n2, "Link 1" ) )
        return g, n2, n3

class LinkDirectionDifference( unittest.TestCase, DifferenceTestCase ):
    def createGraph1( self ):
        g, n2, n3 = self.createBasicGraph()
        g.add( Link( n3, n2, "Link 2" ) )
        return g

    def createGraph2( self ):
        g, n2, n3 = self.createBasicGraph()
        g.add( Link( n2, n3, "Link 2" ) )
        return g

    def createBasicGraph( self ):
        g = Graph( "Nodes and links" )
        n1 = Node( "Node 1" )
        g.add( n1 )
        n2 = Node( "Node 2" )
        g.add( n2 )
        n3 = Node( "Node 3" )
        g.add( n3 )
        g.add( Link( n1, n2, "Link 1" ) )
        return g, n2, n3

class OneMoreNodeDifference( unittest.TestCase, DifferenceTestCase ):
    def createGraph1( self ):
        return self.createBasicGraph()

    def createGraph2( self ):
        g = self.createBasicGraph()
        g.add( Node( "Node 4" ) )
        return g

    def createBasicGraph( self ):
        g = Graph( "Nodes and links" )
        n1 = Node( "Node 1" )
        g.add( n1 )
        n2 = Node( "Node 2" )
        g.add( n2 )
        n3 = Node( "Node 3" )
        g.add( n3 )
        g.add( Link( n1, n2, "Link 1" ) )
        g.add( Link( n2, n3, "Link 2" ) )
        return g

class NodeNameDifference( unittest.TestCase, DifferenceTestCase ):
    def createGraph1( self ):
        g = self.createBasicGraph()
        g.add( Node( "Node 4" ) )
        return g

    def createGraph2( self ):
        g = self.createBasicGraph()
        g.add( Node( "Node 4 bis" ) )
        return g

    def createBasicGraph( self ):
        g = Graph( "Nodes and links" )
        n1 = Node( "Node 1" )
        g.add( n1 )
        n2 = Node( "Node 2" )
        g.add( n2 )
        n3 = Node( "Node 3" )
        g.add( n3 )
        g.add( Link( n1, n2, "Link 1" ) )
        g.add( Link( n2, n3, "Link 2" ) )
        return g

class GraphNameDifference( unittest.TestCase, DifferenceTestCase ):
    def createGraph1( self ):
        return Graph( "Graph 1" )

    def createGraph2( self ):
        return Graph( "Graph 2" )

class GraphAttributeDifference( unittest.TestCase, DifferenceTestCase ):
    def createGraph1( self ):
        g = Graph( "Graph" )
        g.attr[ "foobar" ] = "foobar"
        return g

    def createGraph2( self ):
        g = Graph( "Graph" )
        g.attr[ "foobar" ] = "barbaz"
        return g

class GraphNodeAttributeDifference( unittest.TestCase, DifferenceTestCase ):
    def createGraph1( self ):
        g = Graph( "Graph" )
        g.nodeAttr[ "foobar" ] = "foobar"
        return g

    def createGraph2( self ):
        g = Graph( "Graph" )
        g.nodeAttr[ "foobar" ] = "barbaz"
        return g

class GraphEgdeAttributeDifference( unittest.TestCase, DifferenceTestCase ):
    def createGraph1( self ):
        g = Graph( "Graph" )
        g.edgeAttr[ "foobar" ] = "foobar"
        return g

    def createGraph2( self ):
        g = Graph( "Graph" )
        g.edgeAttr[ "foobar" ] = "barbaz"
        return g

unittest.main()
