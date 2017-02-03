from slackclient import SlackClient
from urllib import urlencode
import requests
SLACK_API_URL = "https://slack.com/api/%s?%s"

def make_url(base, **parms):
    return SLACK_API_URL % (base, urlencode(parms))

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
        if self._username is None or self._emoji is None:
            self._client.api_call("chat.postMessage",channel=receipt,text=text,
                                  as_user=True)
        else:
            self._client.api_call("chat.postMessage",channel=receipt,text=text,
                                  username=self._username, icon_emoji=self._emoji)

    def upload_file(self, receipt, filepath):
        requrl = make_url("files.upload",token=self._token,
                          filename=filepath,filetype="png")
        if self._username is None or self._emoji is None:
            data= {"channels":[receipt], "as_user":True}
        else:
            data= {"channels":[receipt], "username":self._username, "icon_emoji":self._emoji, "as_user":False}
        resp = requests.post(requrl, files={"file":open(filepath,'rb')}, data=data)


