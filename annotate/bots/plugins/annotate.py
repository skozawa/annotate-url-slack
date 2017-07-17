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
        'fallback': 'Fallback text',
        'author_name': 'Author',
        'author_link': 'http://www.github.com',
        'text': 'Some text',
        'color': '#59afe1'
    }]
    message.send_webapi('', json.dumps(attachments))


@listen_to('test')
def test(message):
    attachments = [
        {
            "text": "Choose a game to play",
            "fallback": "You are unable to choose a game",
            "callback_id": "wopr_game",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "game",
                    "text": "Chess",
                    "type": "button",
                    "value": "chess"
                },
                {
                    "name": "game",
                    "text": "Falken's Maze",
                    "type": "button",
                    "value": "maze"
                }
            ]
        }
    ]
    message.send_webapi('', json.dumps(attachments))

