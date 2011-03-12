import os.path

rootDirectory = os.path.relpath( os.path.dirname( os.path.dirname( os.path.dirname( os.path.realpath( __file__ ) ) ) ) )

libDirectory = os.path.join( rootDirectory, "lib" )

buildkitsDirectory = os.path.join( rootDirectory, "Buildkits" )

toolsetsDirectory = os.path.join( rootDirectory, "Toolsets" )
toolsetsTmpDirectory = os.path.join( toolsetsDirectory, "Build" )
toolsetsInstallDirectory = os.path.join( toolsetsDirectory, "Install" )

toolsDirectory = os.path.join( toolsetsDirectory, "Tools" )
toolsCacheDirectory = os.path.join( toolsDirectory, "Cache" )
