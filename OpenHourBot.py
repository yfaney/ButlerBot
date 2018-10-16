#!/usr/local/bin/python

import re, requests
from pyquery import PyQuery
from datetime import datetime
from babel import Locale

import sys

import SlackBot

from utils.configmanager import ConfigManager

url_urban_air = "https://www.urbanairtrampolinepark.com/locations/kansas/overland-park"

def get_open_hour_urban_air():
    resp = requests.get(url_urban_air)
    pq = PyQuery(resp.content)
    open_hour_raw = pq('div.time')
    print (open_hour_raw)
    open_hour = {}
    for i in range(0,6):
        hour_key = re.sub("\:","",open_hour_raw[i].text.strip())
        open_hour[hour_key] = open_hour_raw[i].getchildren()[0].text.strip()
    return open_hour

"""
====================== Main ===========================
"""
if __name__ == "__main__":
    config = ConfigManager("settings.conf").parse()

    bot = SlackBot.SlackBot(config["Slack"]["Token"])

    urban_air_open_hour = get_open_hour_urban_air()

    if urban_air_open_hour is not None:
        weekday = datetime.today().weekday()
        day_of_today = Locale('ko').days['format']['wide'][weekday]
        bot.send_message(config["Slack"]["ChatroomID"], "<!here|here>")
        bot.send_message(config["Slack"]["ChatroomID"], "주인님, 오늘의 Urban Air 운영시간입니다.")
        bot.send_message(config["Slack"]["ChatroomID"], "%s - %s" % (day_of_today, urban_air_open_hour["Today"]))
