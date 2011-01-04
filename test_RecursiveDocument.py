import unittest
import textwrap

from RecursiveDocument import Document, Section, DefinitionList

class HelpFormating( unittest.TestCase ):
    def testSection( self ):
        main = Document()
        main.add( "Some introduction text blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah" )
        first = Section( "First section" )
        main.add( first )
        first.add( "Some long text blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah" )
        first.add( None )
        first.add( "Some other long text blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah" )
        first.add( None )
        self.assertEquals( main.format(), textwrap.dedent( """\
            Some introduction text blah blah blah blah blah blah blah blah blah
            blah blah blah blah blah blah blah blah blah
            
            First section:
              Some long text blah blah blah blah blah blah blah blah blah blah
              blah blah blah blah blah blah blah blah blah
              
              Some other long text blah blah blah blah blah blah blah blah blah
              blah blah blah blah blah blah blah blah blah blah
        """ ) )

    def testImbricatedSections( self ):
        main = Document()
        main.add( "Some introduction text blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah" )
        first = Section( "First section" )
        main.add( first )
        second = Section( "Second section" )
        first.add( "Some long text blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah" )
        first.add( second )
        second.add( "Some text blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah" )
        first.add( "Some other long text blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah" )
        self.assertEquals( main.format(), textwrap.dedent( """\
            Some introduction text blah blah blah blah blah blah blah blah blah
            blah blah blah blah blah blah blah blah blah
            
            First section:
              Some long text blah blah blah blah blah blah blah blah blah blah
              blah blah blah blah blah blah blah blah blah
            
              Second section:
                Some text blah blah blah blah blah blah blah blah blah blah blah
                blah blah blah blah blah blah blah blah
            
              Some other long text blah blah blah blah blah blah blah blah blah
              blah blah blah blah blah blah blah blah blah blah
        """ ) )

    def testEmptySection( self ):
        main = Document()
        main.add( "Some introduction text blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah" )
        first = Section( "First section" )
        main.add( first )
        second = Section( "Second section" )
        first.add( "Some long text blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah" )
        first.add( second )
        first.add( "Some other long text blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah" )
        self.assertEquals( main.format(), textwrap.dedent( """\
            Some introduction text blah blah blah blah blah blah blah blah blah
            blah blah blah blah blah blah blah blah blah
            
            First section:
              Some long text blah blah blah blah blah blah blah blah blah blah
              blah blah blah blah blah blah blah blah blah
            
              Second section:
            
              Some other long text blah blah blah blah blah blah blah blah blah
              blah blah blah blah blah blah blah blah blah blah
        """ ) )

    def testEmptyList( self ):
        main = Document()
        list = DefinitionList()
        definitions = Section( "Definitions" )
        main.add( definitions )
        definitions.add( list )
        self.assertEquals( main.format(), textwrap.dedent( """\
        Definitions:
        """ ) )

    def testList( self ):
        main = Document()
        list = DefinitionList()
        definitions = Section( "Definitions" )
        main.add( definitions )
        definitions.add( list )
        list.add( "item1", "definition1 blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah" )
        list.add( "long-item2", "definition2" )
        list.add( "item3", "definition3" )
        self.assertEquals( main.format(), textwrap.dedent( """\
        Definitions:
          item1       definition1 blah blah blah blah blah blah blah blah blah
                      blah blah blah blah blah blah blah blah blah blah
          long-item2  definition2
          item3       definition3
        """ ) )

    def testEmptyDefinition( self ):
        main = Document()
        list = DefinitionList()
        definitions = Section( "Definitions" )
        main.add( definitions )
        definitions.add( list )
        list.add( "item1", "definition1 blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah" )
        list.add( "long-item2", "" )
        list.add( "item3", "definition3" )
        self.assertEquals( main.format(), textwrap.dedent( """\
        Definitions:
          item1       definition1 blah blah blah blah blah blah blah blah blah
                      blah blah blah blah blah blah blah blah blah blah
          long-item2
          item3       definition3
        """ ) )

    def testListWithLongestShortEnoughtItem( self ):
        main = Document()
        list = DefinitionList()
        definitions = Section( "Definitions" )
        main.add( definitions )
        definitions.add( list )
        list.add( "long-item1", "definition1 blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah" )
        list.add( "-very-very-very-long-item2", "definition2 blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah" )
        list.add( "item3", "definition3 blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah" )
        self.assertEquals( main.format(), textwrap.dedent( """\
        Definitions:
          long-item1                  definition1 blah blah blah blah blah
                                      blah blah blah blah blah blah blah blah
                                      blah blah
          -very-very-very-long-item2  definition2 blah blah blah blah blah
                                      blah blah blah blah blah blah blah blah
                                      blah blah
          item3                       definition3 blah blah blah blah blah
                                      blah blah blah blah blah blah blah blah
                                      blah blah blah blah blah blah blah blah
                                      blah blah blah blah blah blah blah blah
                                      blah
        """ ) )
    
    def testListWithJustTooLongItem( self ):
        main = Document()
        list = DefinitionList()
        definitions = Section( "Definitions" )
        main.add( definitions )
        definitions.add( list )
        list.add( "long-item1", "definition1 blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah" )
        list.add( "--very-very-very-long-item2", "definition2 blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah" )
        list.add( "item3", "definition3 blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah" )
        self.assertEquals( main.format(), textwrap.dedent( """\
        Definitions:
          long-item1  definition1 blah blah blah blah blah blah blah blah blah
                      blah blah blah blah blah blah
          --very-very-very-long-item2
                      definition2 blah blah blah blah blah blah blah blah blah
                      blah blah blah blah blah blah
          item3       definition3 blah blah blah blah blah blah blah blah blah
                      blah blah blah blah blah blah blah blah blah blah blah
                      blah blah blah blah blah blah blah blah blah blah
        """ ) )

unittest.main()
