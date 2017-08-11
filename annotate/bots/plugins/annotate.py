from slackbot.bot import respond_to
from slackbot.bot import listen_to
import json
import re

from annotate.db import DB
from annotate.slack.response import OptionsResponse

import annotate.service.entry as entry_service
import annotate.service.annotation as annotation_service

@respond_to('help', re.IGNORECASE)
def help(message):
    message.send('Post url')


@listen_to('<(https?://[^>]+)>')
def listen_url(message, url=None):
    db = DB()
    scores = _get_scores(db, url, message._client.users[message.body['user']]['name'])
    db.close()
    res = OptionsResponse(url, scores=scores)
    message.send_webapi(res.text(), json.dumps(res.attachments()))

def _get_scores(db, url, annotator):
    entry = entry_service.find_by_url(db, url)
    if entry is None:
        return {}
    annotation = annotation_service.find_by_id_and_annotator(db, entry.id, annotator)
    if annotation is None:
        return {}
    return annotation.score()
