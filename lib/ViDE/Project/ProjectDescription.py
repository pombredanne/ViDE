# -*- coding: utf-8 -*-


class ProjectDescription:
    def __init__(self, name):
        self.name = name


class ProjectBuilder:
    def __init__(self):
        self.name = None

    def describeProject(self, name):
        self.name = name

    def parseString(self, s):
        d = {
            "Project": self.describeProject
        }
        exec s in d

    def createProject(self):
        return ProjectDescription(self.name)

def fromString(s):
    b = ProjectBuilder()
    b.parseString(s)
    return b.createProject()
