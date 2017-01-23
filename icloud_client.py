from pyicloud import PyiCloudService
from datetime import datetime, timedelta

class iclient:
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._api = PyiCloudService(self._username, self._password)

    def get_agenda(self, mdate):
        return self._api.calendar.events(mdate, mdate)

    def get_today_agenda(self):
        return self.get_agenda(datetime.today(), datetime.today())

    def get_tomorrow_agenda(self):
        return self.get_agenda(datetime.today() + timedelta(1), datetime.today() + timedelta(1))

    def get_this_month_schedule(self):
        return self._api.calendar.events()

