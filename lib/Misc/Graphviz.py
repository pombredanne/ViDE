def attributesDotString( attr, sep = "," ):
    return sep.join( sorted( k + "=\"" + attr[ k ] + "\"" for k in attr ) )

class Container:
    def __init__( self ):
        self.__nodes = set()

    def add( self, element ):
        if isinstance( element, Node ) or isinstance( element, Cluster ):
            self.__nodes.add( element )
        else:
            raise Exception( "Unknown element type:" + element.__class__.__name__ )

    def getOneNode( self ):
        for n in self.__nodes:
             return n.getOneNode()

    def contentDotString( self ):
        return "".join( sorted( n.dotString() for n in self.__nodes ) )

    ### BUG: if two nodes have the same attributes, they may get inverted in the map, 
    # and Link.areSame will not work
    @staticmethod
    def haveSameNodes( left, right ):
        if len( left.__nodes ) != len( right.__nodes ):
            return False, None
        map = dict()
        leftNodes = left.__nodes
        rightNodes = set( right.__nodes )
        for leftNode in leftNodes:
            for rightNode in rightNodes:
                if isinstance( leftNode, Node ) and isinstance( rightNode, Node ) and Node.areSame( leftNode, rightNode ):
                    map[ leftNode ] = rightNode
                    rightNodes.remove( rightNode )
                    break
                if isinstance( leftNode, Container ) and isinstance( rightNode, Container ):
                    same, subMap = Container.haveSameNodes( leftNode, rightNode )
                    if same:
                        map[ leftNode ] = rightNode
                        map.update( subMap )
                        rightNodes.remove( rightNode )
                        break
        return len( rightNodes ) == 0, map

class Graph( Container ):
    def __init__( self, name ):
        Container.__init__( self )
        self.__name = name
        self.nodeAttr = dict()
        self.edgeAttr = dict()
        self.attr = { "compound": "true" }
        self.__links = set()

    def add( self, element ):
        if isinstance( element, Link ):
            self.__links.add( element )
        else:
            Container.add( self, element )

    def dotString( self ):
        return ( 
            "digraph \"" + self.__name + "\" {" + attributesDotString( self.attr, ";" )
            + ";node [" + attributesDotString( self.nodeAttr ) 
            + "];edge [" + attributesDotString( self.edgeAttr ) + "];" 
            + self.contentDotString() 
            + "".join( sorted( l.dotString() for l in self.__links ) )
            + "}"
        )

    @staticmethod
    def areSame( left, right ):
        if left.__name != right.__name or left.attr != right.attr or left.nodeAttr != right.nodeAttr or left.edgeAttr != right.edgeAttr:
            return False
        same, map = Container.haveSameNodes( left, right )
        if not same:
            return False
        return Graph.__haveSameLinks( left, right, map )

    @staticmethod
    def __haveSameLinks( left, right, map ):
        if len( left.__links ) != len( right.__links ):
            return False
        leftLinks = left.__links
        rightLinks = set( right.__links )
        for leftLink in leftLinks:
            for rightLink in rightLinks:
                if Link.areSame( leftLink, rightLink, map ):
                    rightLinks.remove( rightLink )
                    break
        return len( rightLinks ) == 0

class Cluster( Container ):
    nextId = 0
    def __init__( self, label ):
        Container.__init__( self )
        self.__id = Cluster.nextId
        Cluster.nextId += 1
        self.attr = { "label": label }

    def dotString( self ):
        return "subgraph " + self.id() + "{" + attributesDotString( self.attr, ";" ) + ";" + self.contentDotString() + "};"

    def id( self ):
        return "cluster_" + str( self.__id )

class Node:
    nextId = 0
    def __init__( self, label ):
        self.__id = Node.nextId
        Node.nextId += 1
        self.attr = { "label": label }

    def dotString( self ):
        return self.id() + "[" + attributesDotString( self.attr ) + "];"

    def getOneNode( self ):
        return self

    def id( self ):
        return "node_" + str( self.__id )

    @staticmethod
    def areSame( left, right ):
        return left.attr == right.attr

class Link:
    def __init__( self, origin, destination, label = None ):
        self.attr = {}
        if label is not None:
            self.attr[ "label" ] = label
        if isinstance( origin, Cluster ):
            self.__origin = origin.getOneNode()
            self.__originCluster = origin
            self.attr[ "ltail" ] = origin.id()
        else:
            self.__origin = origin
            self.__originCluster = None
        if isinstance( destination, Cluster ):
            self.__destination = destination.getOneNode()
            self.__destinationCluster = destination
            self.attr[ "lhead" ] = destination.id()
        else:
            self.__destination = destination
            self.__destinationCluster = None

    def dotString( self ):
        return self.__origin.id() + "->" + self.__destination.id() + "[" + attributesDotString( self.attr ) + "];"

    @staticmethod
    def areSame( left, right, map ):
        leftAttr = dict( left.attr )
        rightAttr = dict( right.attr )
        leftAttr.pop( "lhead", "" ) # Default value given, to avoid an exception when lhead is not in leftAttr
        leftAttr.pop( "ltail", "" )
        rightAttr.pop( "lhead", "" )
        rightAttr.pop( "ltail", "" )
        ### @todo Cover each "return False" in unit tests
        if leftAttr != rightAttr:
            return False
        if left.__originCluster is None:
            if right.__originCluster is not None:
                return False
            if map[ left.__origin ] != right.__origin:
                return False
        else:
            if right.__originCluster is None:
                return False
            if map[ left.__originCluster ] != right.__originCluster:
                return False
        if left.__destinationCluster is None:
            if right.__destinationCluster is not None:
                return False
            if map[ left.__destination ] != right.__destination:
                return False
        else:
            if right.__destinationCluster is None:
                return False
            if map[ left.__destinationCluster ] != right.__destinationCluster:
                return False
        return True
