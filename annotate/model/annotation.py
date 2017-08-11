import json

class Annotation(object):
    def __init__(self, args):
        self.entry_id = args.get('entry_id', None)
        self.annotator = args.get('annotator', None)
        self.score_raw = args.get('score', None)
        self._score = None
        self.created = args.get('created', None)
        self.modified = args.get('modified', None)

    def score(self):
        if self._score is None:
            try:
                self._score = json.loads(self.score_raw)
            except Exception:
                self._score = {}
        return self._score
