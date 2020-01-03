#!/usr/local/bin/python

import re, requests, json

import sys

import SlackBot
import telegram

from utils.configmanager import ConfigManager

url_pick_n_pull = "http://www.picknpull.com"

PICKNPULL_INVENTORY = "check_inventory.aspx"
PICKNPULL_REX = '(mydata_[0-9]+[ ]=[ ])([\\[\\{\\"\\w:,\\- \\(\\)./\\}\\]]+);'
PICKNPULL_BMW3S = "Make=90&Model=1150&Year=2013-18"
PICKNPULL_BMW3W = "Make=90&Model=1151&Year=2013-18"
PICKNPULL_BMW5S = "Make=90&Model=1152&Year=2010-17"
PICKNPULL_BMW5W = "Make=90&Model=1154&Year=2010-17"

def check_inventory(zipcode, modelyear):
    req_url = "%s/%s?Zip=%s&%s&Distance=25" % (url_pick_n_pull, PICKNPULL_INVENTORY, zipcode, modelyear)
    resp = requests.get(req_url)
    if resp.status_code == 200:
        result = resp.content.decode("utf-8")
        match = re.findall(PICKNPULL_REX, result)
        if len(match) > 0:
            vehicle_list = []
            for item in match:
                vehicle_list.append(json.loads(item[1])[0])
            return vehicle_list
        else:
            return []

"""
====================== Main ===========================
"""
if __name__ == "__main__":
    config = ConfigManager("settings.conf").parse()

    bot = SlackBot.SlackBot(config["Slack"]["Token"])
    tbot = telegram.Bot(token=config["Telegram"]["Token"])
    slack_chatroom_id = config["Slack"]["ChatroomID"]
    telegram_chatroom_id = config["Telegram"]["ChatroomID"]
    zipcode = config["Location"]["zipcode"]

    vehicle_list = check_inventory(zipcode, PICKNPULL_BMW3S)
    vehicle_list = [*vehicle_list, *check_inventory(zipcode, PICKNPULL_BMW3W)]
    vehicle_list = [*vehicle_list, *check_inventory(zipcode, PICKNPULL_BMW5S)]
    vehicle_list = [*vehicle_list, *check_inventory(zipcode, PICKNPULL_BMW5W)]

    if len(vehicle_list) > 0:
        bot.send_message(slack_chatroom_id, "<!here|here>")
        list_msg = []
        for vehicle in vehicle_list:
            list_msg.append("(%s)%s %s %s" % (vehicle['VIN'], vehicle['Year'], vehicle['Make'], vehicle['Model']))
        payload = "주인님, PickNPull에 재고가 있습니다.\n%s" % '\n'.join(list_msg)
        print(payload)
        bot.send_message(slack_chatroom_id, payload)
        tbot.send_message(chat_id=telegram_chatroom_id, text=payload)
    else:
        print("No vehicles available at this point.")
