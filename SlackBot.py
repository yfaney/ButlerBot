from slackclient import SlackClient

class SlackBot:
    def __init__(self, token=None):
        self._token = token
        self._client = SlackClient(self._token)
        self._username = None
        self._emoji = None

    def set_user_info(self, username, emoji):
        self._username = username
        self._emoji = emoji

    def list_channels(self):
        channels_call = self._client.api_call("channels.list")
        if channels_call.get('ok'):
            return channels_call['channels']
        return None

    def send_message(self, receipt, text):
        if self._username is None or self._emiji is None:
            self._client.api_call("chat.postMessage",channel=receipt,text=text,
                                  as_user=True)
        else:
            self._client.api_call("chat.postMessage",channel=receipt,text=text,
                                  username=self._username, icon_emoji=self._emoji)

