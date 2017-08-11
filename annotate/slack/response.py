from annotate.config import config
from annotate.spread import Gspread

class OptionsResponse(object):
    def __init__(self, url, name="metrics", callback_id="quality_metrics", color="#3AA3E3", scores=None):
        self.url = url
        self.name = name
        self.callback_id = callback_id
        self.color = color
        self.values = config.METRICS.copy()
        self._scores = scores

    @property
    def scores(self):
        if self._scores is None:
            gspread = Gspread()
            self._scores = gspread.url_score(self.url)
        return self._scores

    def response(self):
        return {'text': self.text(), 'attachments': self.attachments()}

    def text(self):
        return 'Annotate URL: ' + self.url

    def attachments(self):
        return [
            {
                "fallback": "If you could read this message, you'd be choosing something fun to do right now.",
                "color": self.color,
                "attachement_type": "default",
                "callback_id": self.callback_id,
                "actions": [
                    {
                        "name": self.name,
                        "text": "Select...",
                        "type": "select",
                        "options": [self._option(v) for v in self.values]
                    }
                ]
            }
        ]

    def _option(self, value):
        return {'text': self._option_text(value), 'value': value}

    def _option_text(self, value):
        score = self.scores.get(value, None)
        if score is None:
            return value
        return "%s [%d]" % (value, score)


class EvaluateResponse(object):
    def __init__(self, value, url=''):
        self.value = value
        self.url   = url
        self.level = 5

    def response(self):
        return {'text': self.text(), 'attachments': self.attachments()}

    def text(self):
        return 'Annotate URL: ' + self.url

    def attachments(self):
        return [
            {
                'text': self.value,
                'callback_id': 'evaluate_metric',
                'attachement_type': 'default',
                'actions': [self._action(level) for level in range(1, self.level + 1)]
            }
        ]

    def _action(self, level):
        return {
            'name': 'score',
            'text': str(level),
            'type': 'button',
            'value': level
        }
