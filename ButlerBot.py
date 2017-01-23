#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys

import SlackBot
import icloud_client
import PrivateResource
import WeatherUG

from utils.configmanager import ConfigManager



MY_TOKEN = PrivateResource.MY_TOKEN
#BUTLER_NAME = PrivateResource.BUTLER_NAME
#BUTLER_EMOJI = PrivateResource.BUTLER_EMOJI
CHATROOM_ID = PrivateResource.CHATROOM_ID
ICLOUD_ID = PrivateResource.ICLOUD_ID
ICLOUD_PW = PrivateResource.ICLOUD_PW
ZIPCODE = PrivateResource.ZIPCODE

#bot.set_username(BUTLER_NAME)
#bot.set_emoji(":%s:" % BUTLER_EMOJI)

def send_message(message):
    bot.send_message(config["Slack"]["ChatroomID"], message)


def get_today_agenda():
    agenda = client.get_today_agenda()
    #agenda = client.get_this_month_schedule()
    return agenda

def get_tomorrow_agenda():
    agenda = client.get_tomorrow_agenda()
    return agenda

def gen_greeting(night=False):
    if night:
        return u"@here\n안녕하십니까 주인님. 오늘도 수고하셨습니다."
    else:
        return u"@here\n안녕하십니까 주인님. 좋은 아침입니다."

def gen_end_msg(night=False):
    if night:
        return u"그럼 좋은 밤 되십시오."
    else:
        return u"그럼 좋은 하루 되십시오."

def gen_agenda_message(night=False):
    if night:
        agenda = get_tomorrow_agenda()
        mdate = u"내일"
    else:
        agenda = get_today_agenda()
        mdate = u"오늘"
    msgs = []
    if agenda is None or len(agenda) == 0:
        return u"%s은 특별한 일정이 없습니다." % mdate
    else:
        msgs.append(u"%s 일정을 말씀드리겠습니다.\n" % mdate)
    first_item = True
    count = 1
    for item in agenda:
        if first_item:
            msgs.append(u"%s은" % mdate)
            first_item = False
        if item["allDay"]:
            continue
        msgs.append(u"%s시 %s분부터" % (item["startDate"][4], item["startDate"][5]))
        msgs.append(u"%s시 %s분까지" % (item["endDate"][4], item["endDate"][5]))
        if item["location"] is not None:
            msgs.append(u"%s에서" % item["location"])
        msgs.append(u"%s 일정이" % item["title"])
        if count < len(agenda):
            msgs.append(u"있으시고,")
        count = count +1
    msgs.append(u"있으십니다.")
    return " ".join(msgs)

def populate_weather(wtext):
    popul = {"Partly Cloudy": u"약간 흐릴", "Overcast": u"흐릴", "Sunny": u"맑을", "Rainy": u"비가 올", "Snowy": u"눈이 올"}
    try:
        return popul[wtext]
    except Exception,e:
        return wtext

def gen_forecast(night=False):
    try:
        if(night):
            mdate = u"내일"
            overall = WeatherUG.getWeeklyFC_Overall(ZIPCODE, 1)
            qpf_day = None
        else:
            mdate = u"오늘"
            overall = WeatherUG.getWeeklyFC_Overall(ZIPCODE, 0)
            qpf_day = WeatherUG.getHourlyFC_QPF(ZIPCODE)
    except Exception, e:
        print "Exception %s with message '%s' occurred." % (type(e), str(e))
        return ""
    fcmsg = []
    fcmsg.append(u"%s은 대체로 %s 예정이고 최대 %s도, 최저 %s도일 것으로 예상됩니다." % (mdate, populate_weather(overall["condition"]), overall["temp_high"], overall["temp_low"]))
    if qpf_day is not None and len(qpf_day) > 0:
        fcmsg.append(u"또한, 금일 중 비가")
        qpfm = []
        for qpf in qpf_day:
            qpfm.append(u"%s시에 %smm" % (qpf["hour"], qpf["qpf"]))
        fcmsg.append(u"%s 내릴 수 있으니 외출시 우산 잊지 마십시오." % (", ".join(qpfm)))
    return " ".join(fcmsg)

"""
====================== Main ===========================
"""
if __name__ == "__main__":
    if len(sys.argv) > 1:
        greet = sys.argv[1]
    else:
        greet = None

    bot_msg = []

    DAY_OR_NIGHT = greet == "night"
    config = ConfigManager("settings.conf").parse()
    msg = ConfigManager("messages.conf").parse()

    iclient = icloud_client.iclient(config["iCloud"]["ID"], config["iCloud"]["PW"])
    bot = SlackBot.SlackBot(config["Slack"]["Token"])

    bot_msg.append(gen_greeting(DAY_OR_NIGHT))
    bot_msg.append(gen_agenda_message(DAY_OR_NIGHT))
    bot_msg.append(gen_forecast(DAY_OR_NIGHT))
    bot_msg.append(gen_end_msg(DAY_OR_NIGHT))

    for m in bot_msg:
        #print m
        bot.send_message(config["Slack"]["ChatroomID", m)
