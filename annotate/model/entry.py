class Entry(object):
    def __init__(self, args):
        self.id = args.get('id', None)
        self.uri = args.get('uri', None)
        self.created = args.get('created', None)
