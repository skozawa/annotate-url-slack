from slackbot.bot import respond_to
from slackbot.bot import listen_to
import json
import re

@respond_to('help', re.IGNORECASE)
def help(message):
    message.send('Post url')


@listen_to('<(https?://[^>]+)>')
def listen_url(message, url=None):
    # Message is sent on the channel
    message.send(url)
    attachments = [
        {
            "text": "Do you annotate this url: %s" % (url),
            "fallback": "You are unable to choose",
            "callback_id": "annotate_url_request",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "annotate_url",
                    "text": "Yes",
                    "type": "button",
                    "value": "yes"
                },
                {
                    "name": "annotate_url",
                    "text": "No",
                    "type": "button",
                    "value": "not"
                }
            ]
        }
    ]
    message.send_webapi('', json.dumps(attachments))
