import os.path
import re
import sys
import itertools

from ViDE.Core.Artifact import AtomicArtifact
from ViDE.Project.Project import Project
from ViDE.Project.Artifacts.BasicArtifacts import MonofileInputArtifact

class Source( MonofileInputArtifact ):
    pass

class Object( AtomicArtifact ):
    def __init__( self, buildkit, files, source, explicit ):
        AtomicArtifact.__init__(
            self,
            name = files[ 0 ],
            files = files,
            strongDependencies = [ source ],
            orderOnlyDependencies = [],
            automaticDependencies = [],
            explicit = explicit
        )
        self.__source = source

    def getSource( self ):
        return self.__source
