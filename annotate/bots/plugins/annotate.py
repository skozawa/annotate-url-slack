from slackbot.bot import respond_to
from slackbot.bot import listen_to
import json
import re

from annotate.slack.response import OptionsResponse

@respond_to('help', re.IGNORECASE)
def help(message):
    message.send('Post url')


@listen_to('<(https?://[^>]+)>')
def listen_url(message, url=None):
    res = OptionsResponse(url)
    message.send_webapi(res.text(), json.dumps(res.attachments()))
