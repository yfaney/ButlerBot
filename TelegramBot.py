import telegram

class TelegramBot:
    def __init__(self, token=None):
        self._token = token
        self._client = telegram.Bot(token=self._token)

    def send_message(self, receipt, text):
        self._client.send_message(chat_id=receipt, text=text)

    def send_markdown_message(self, receipt, text):
        self._client.send_message(chat_id=receipt, text=text, parse_mode="Markdown")

    def send_html_message(self, receipt, text):
        self._client.send_message(chat_id=receipt, text=text, parse_mode="HTML")

    def send_picture(self, receipt, filepath):
        with open(filepath, 'rb') as f:
            return self._client.send_photo(receipt, photo=f, timeout=50).photo

    def send_video(self, receipt, filepath):
        with open(filepath, 'rb') as f:
            return self._client.send_video(receipt, video=f, timeout=50).video
