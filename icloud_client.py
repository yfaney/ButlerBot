from pyicloud import PyiCloudService
from datetime import datetime

class iclient:
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._api = PyiCloudService(self._username, self._password)

    def get_today_agenda(self):
        return self._api.calendar.events(datetime.today(), datetime.today())

    def get_this_month_schedule(self):
        return self._api.calendar.events()

