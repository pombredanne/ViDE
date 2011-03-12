import os.path

rootDirectory = os.path.relpath( os.path.dirname( os.path.dirname( os.path.dirname( os.path.realpath( __file__ ) ) ) ) )

libDirectory = os.path.join( rootDirectory, "lib" )

buildkitsDirectory = os.path.join( rootDirectory, "Buildkits" )

toolsetsDirectory = os.path.join( rootDirectory, "Toolsets" )

toolsDirectory = os.path.join( toolsetsDirectory, "Tools" )

toolsCacheDirectory = os.path.join( toolsDirectory, "Cache" )
