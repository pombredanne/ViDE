# -*- coding: utf-8 -*-

import Artifacts


class ProjectDescription:
    def __init__(self, name, artifacts):
        self.name = name
        self.artifacts = artifacts


class ProjectBuilder:
    def __init__(self):
        self.name = None
        self.artifacts = []

    def describeProject(self, name):
        self.name = name

    def createArtifact(self, factory, *a, **k):
        artifact = factory(*a, **k)
        self.artifacts.append(artifact)
        return artifact

    def __createArtifact(self, factory):
        return lambda *a, **k: self.createArtifact(factory, *a, **k)

    def parseString(self, s):
        d = {"Project": self.describeProject}
        for factory in Artifacts.allFactories:
            d[factory.__name__] = self.__createArtifact(factory)
        exec s in d

    def createProject(self):
        return ProjectDescription(self.name, self.artifacts)


def fromString(s):
    b = ProjectBuilder()
    b.parseString(s)
    return b.createProject()
