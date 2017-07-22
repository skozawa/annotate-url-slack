from datetime import datetime
import re

import annotate.slack.response as slack_res


class SlackRequest(object):
    def __init__(self, payload):
        self.payload = payload

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
    def actions(self):
        return self.payload.get('actions', [])

    @property
    def original_message(self):
        return self.payload.get('original_message', {})

    @property
    def original_text(self):
        return self.original_message.get('text', '')

    @property
    def original_attachments_text(self):
        attachments = self.original_message.get('attachments', [])
        if not attachments:
            return ''
        return attachments[0].get('text', '')

    def resource_url(self):
        text = self.original_message.get('text', '')
        match = re.compile('<(https?://[^>]+)>').search(text)
        return match.group(1)


class ActionRequest(SlackRequest):
    def action_is_ok(self):
        actions = self.actions
        if len(actions) == 1 and actions[0].get('value', '') == 'yes':
            return True
        return False

    @property
    def response_url(self):
        return self.payload.get('response_url')

    def response(self):
        if not self.action_is_ok():
            return {'text': ':x:'}
        return {'text': ':o:'}


class EvaluateMetricRequest(ActionRequest):
    def response(self):
        res = slack_res.OptionsResponse(self.resource_url(), scores=self.scores())
        return {'text': res.text(), 'attachments': res.attachments()}

    def scores(self):
        scores = {}
        scores[self.attr()] = self.value()
        return scores

    def value(self):
        if not self.actions:
            return 0
        return self.actions[0].get('value', 0)

    def attr(self):
        return self.original_attachments_text


class OptionsRequest(SlackRequest):
    @property
    def name(self):
        return self.payload.get('name', '')

    @property
    def value(self):
        if not self.actions:
            return ''
        selected_options = self.actions[0].get('selected_options', [])
        if not selected_options:
            return ''
        return selected_options[0].get('value', '')


class QualityMetricsRequest(OptionsRequest):
    def response(self):
        res = slack_res.EvaluateResponse(self.value)
        return {'text': res.text(self.resource_url()), 'attachments': res.attachments()}

