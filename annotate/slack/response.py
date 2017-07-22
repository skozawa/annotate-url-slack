class OptionsResponse(object):
    def __init__(self, url, name="metrics", callback_id="quality_metrics", color="#3AA3E3", scores={}):
        self.url = url
        self.name = name
        self.callback_id = callback_id
        self.color = color
        self.values = ['Quality', 'Readability', 'Informativeness', 'Style', 'Topic', 'Sentiment']
        self.scores = scores

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
