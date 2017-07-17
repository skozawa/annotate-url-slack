from datetime import datetime

class ActionRequest(object):
    def __init__(self, payload):
        self.payload = payload

    @property
    def actions(self):
        return self.payload.get('actions', [])

    def action_is_ok(self):
        actions = self.actions
        if len(actions) == 1 and actions[0].get('value', '') == 'yes':
            return True
        return False

    @property
    def callback_id(self):
        return self.payload.get('callback_id')

    @property
    def team_id(self):
        return self.payload.get('team', {}).get('id')

    @property
    def team_domain(self):
        return self.payload.get('team', {}).get('domain')

    @property
    def channel_id(self):
        return self.payload.get('channel', {}).get('id')

    @property
    def channel_name(self):
        return self.payload.get('channel', {}).get('name')

    @property
    def user_id(self):
        return self.payload.get('user', {}).get('id')

    @property
    def user_name(self):
        return self.payload.get('user', {}).get('name')

    @property
    def action_dt(self):
        if self._action_dt is None:
            self._action_dt = datetime.fromtimestamp(self.payload.get('action_ts', 0))
        return self._action_dt

    @property
    def message_dt(self):
        if self._message_dt is None:
            self._message_dt = datetime.fromtimestamp(self.payload.get('message_ts', 0))
        return self._message_dt

    @property
    def original_message(self):
        return self.payload.get('original_message', {})

    @property
    def original_text(self):
        attachments = self.original_message.get('attachments', [])
        return attachments[0].get('text', '')

    @property
    def response_url(self):
        return self.payload.get('response_url')

    def response(self):
        if not self.action_is_ok():
            return {'text': ':x:'}
        return {'text': ':o:'}


class AnnotateUrlRequest(ActionRequest):
    def response(self):
        if not self.action_is_ok():
            return {'text': ':x:'}
        return {'text': self.original_text, 'attachments': [self.attachment(target) for target in ['reading', 'funny', 'topic', 'completely']]}

    def attachment(self, target):
        return {
            "text": target,
            "callback_id": "annotation_%s" % (target),
            "attachment_type": "default",
            "replace_original": False,
            "actions": [self._action(level) for level in range(1, 6)]
        }

    def _action(self, level):
        return {
            'name': 'score',
            'text': str(level),
            'type': 'button',
            'value': int(level)
        }
