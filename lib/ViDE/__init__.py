import os.path

rootDirectory = os.path.dirname( os.path.dirname( os.path.dirname( os.path.realpath( __file__ ) ) ) )

libDirectory = os.path.join( rootDirectory, "lib" )

buildKitsDirectory = os.path.join( rootDirectory, "BuildKits" )
