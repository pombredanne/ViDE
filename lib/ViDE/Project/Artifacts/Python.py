class Source:
    def __init__(self, source):
        assert isinstance(source, (str, unicode))


class Script:
    def __init__(self, source):
        assert isinstance(source, Source)


class Module:
    def __init__(self, source, strip):
        assert isinstance(source, Source)


class Package:
    def __init__(self, name, modules):
        assert isinstance(name, (str, unicode))
        assert all(isinstance(module, (Module, CModule)) for module in modules)


class CModule:
    def __init__(self, *a, **k):
        pass
