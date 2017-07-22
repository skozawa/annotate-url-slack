class OptionsResponse(object):
    def __init__(self, url, name="metrics", callback_id="quality_metrics", color="#3AA3E3", scores={}):
        self.url = url
        self.name = name
        self.callback_id = callback_id
        self.color = color
        self.values = ['Quality', 'Readability', 'Informativeness', 'Style', 'Topic', 'Sentiment']
        self.scores = scores

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
        if value not in self.scores:
            return {'text': ':white_medium_square: ' + value, 'value': value}
        return {'text': ':white_square_button: ' + value, 'value': value}


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
