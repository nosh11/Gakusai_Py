def make_constructor(cls):
    def constructor(loader, node):
        data = loader.construct_mapping(node, deep=True)
        return cls.from_dict(data)
    return constructor

def make_representer(tag):
    def representer(dumper, data):
        return dumper.represent_mapping(tag, data.to_dict())
    return representer