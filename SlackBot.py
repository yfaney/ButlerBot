
from slackclient import SlackClient

import PrivateResource

MY_TOKEN = PrivateResource.MY_TOKEN

class SlackBot:
    def __init__(self, token=None):
        if token is None:
            self._token = MY_TOKEN
        else:
            self._token = token
        self._client = SlackClient(self._token)

    def list_channels(self):
        channels_call = slack_client.api_call("channels.list")
        if channels_call.get('ok'):
            return channels_call['channels']
        return None

    def send_message(self, receipt, text, username, emoji):
        self._client.api_call("chat.postMessage",channel=receipt,text=text,
                            username=username, icon_emoji=emoji)

