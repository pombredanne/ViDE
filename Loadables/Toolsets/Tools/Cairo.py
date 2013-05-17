import os.path

from ViDE.Toolset import Tool

from PkgConfig import PkgConfig
from LibSigCpp import LibSigCpp

class Pixman( Tool ):
    def getDependencies( self ):
        return []

class LibPng( Tool ):
    def getDependencies( self ):
        return []

class FreeType( Tool ):
    def getDependencies( self ):
        return []

class FontConfig( Tool ):
    def getDependencies( self ):
        return [ FreeType ]

class Cairo( Tool ):
    def getDependencies( self ):
        return [ Pixman, PkgConfig, LibPng, FontConfig ]

class Cairomm( Tool ):
    def getDependencies( self ):
        return [ Cairo, LibSigCpp ]

    def getIncludeDirectories( self, context ):
        return [ os.path.join( context.toolset.getInstallDirectory(), *path ) for path in [
            ( "include", "sigc++-2.0" ),
            ( "include", "cairo" ),
            ( "include", "freetype2" ),
            ( "lib", "cairomm-1.0", "include" ),
            ( "lib", "sigc++-2.0", "include" ),
            ( "include", "cairomm-1.0" ),
            ( "local", "include", "cairomm-1.0" ),
            ( "local", "lib", "cairomm-1.0", "include" ),
        ] ]

    def getLibPath( self ):
        return "/usr/local/lib"

    def getLibName( self ):
        return "cairomm-1.0"

class PyCairo( Tool ):
    def getDependencies( self ):
        return [ Cairo ]

    def getIncludeDirectories( self, context ):
        return [ os.path.join( context.toolset.getInstallDirectory(), *path ) for path in [
            ( "include", "sigc++-2.0" ),
            ( "include", "pycairo" ),
            ( "include", "cairo" ),
            ( "include", "glib-2.0" ),
            ( "include", "glib-2.0", "include" ),
            ( "include", "pixman-1" ),
            ( "include", "freetype2" ),
            ( "include", "libpng12" ),
            ( "lib", "cairomm-1.0", "include" ),
            ( "lib", "sigc++-2.0", "include" ),
            ( "include", "cairomm-1.0" ),
        ] ]

    def getLibPath( self ):
        return None

    def getLibName( self ):
        return "cairo"
