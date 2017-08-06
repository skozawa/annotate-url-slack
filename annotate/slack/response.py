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
            data = gspread.find_data_by_url(self.url)
            self._scores = {v: int(data[v]) for v in self.values if v in data and data[v]}
        return self._scores

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
        return {'text': self._emoji(self.scores.get(value, 0)) + ' ' + value, 'value': value}

    @staticmethod
    def _emoji(score):
        score_emojis = {
            1: ':one:', 2: ':two:', 3: ':three:',
            4: ':four:', 5: ':five',
        }
        return score_emojis.get(score, ':white_medium_square:')


class EvaluateResponse(object):
    def __init__(self, value):
        self.value = value
        self.level = 5

    def text(self, url):
        return 'Annotate URL: ' + url

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
