import textwrap

class SectionWithContent:
    def __init__( self ):
        self.__content = []

    def add( self, c ):
        self.__content.append( c )

    def formatContent( self, indent ):
        return self.__buildSuite( self.__formatOne( c, indent ) for c in self.__content )

    def __formatOne( self, c, indent ):
        if c is None:
            return []
        if isinstance( c, str ):
            return textwrap.wrap( c, initial_indent = indent, subsequent_indent = indent )
        else:
            return c.formatLines( indent )

    def __buildSuite( self, lists ):
        suite = []
        for l in lists:
            if len( suite ) != 0 and len( l ) != 0:
                suite.append( "" )
            suite += l
        return suite

class Section( SectionWithContent ):
    def __init__( self, title ):
        SectionWithContent.__init__( self )
        self.__title = title

    def formatLines( self, indent ):
        return self.formatTitle( indent ) + self.formatContent( indent + "  " )

    def formatTitle( self, indent ):
        return [ indent + self.__title + ":" ]

class Document( SectionWithContent ):
    def format( self ):
        return "\n".join( self.formatContent( "" ) ) + "\n"

class DefinitionList( Section ):
    def __init__( self ):
        self.__content = []

    def add( self, item, definition ):
        self.__content.append( ( item, definition ) )

    def formatLines( self, indent ):
        lines = []
        if len( self.__content ) != 0:
            longestItem = max( [ 0 ] + [ len( item ) for ( item, definition ) in self.__content if self.__itemIsShortEnought( item, indent ) ] )
            for ( item, definition ) in self.__content:
                initial_indent = indent + item + ( longestItem - len( item ) + 2 ) * " "
                subsequent_indent = indent + ( longestItem + 2 ) * " "
                if definition == "":
                    lines.append( indent + item )
                else:
                    if not self.__itemIsShortEnought( item, indent ):
                        initial_indent = subsequent_indent
                        lines.append( indent + item )
                    lines += textwrap.wrap(
                        definition,
                        initial_indent = initial_indent,
                        subsequent_indent = subsequent_indent
                    )
        return lines

    def __itemIsShortEnought( self, item, indent ):
        return len( item ) + len( indent ) <= 28 # display is 70 characters wide (textwrap), we keep at least 40 chars for definitions, and 2 chars for spacing => at most 70 - 40 - 2 = 28 chars for item
