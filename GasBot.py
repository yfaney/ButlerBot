#!/usr/local/bin/python

import re, requests
from pyquery import PyQuery
from datetime import datetime
from babel import Locale

import sys

import SlackBot
import telegram

from utils.configmanager import ConfigManager

url_gas_buddy = "https://www.gasbuddy.com/home?search=%s&fuel=%s"

GAS_BUDDY_CLASS_STATS = "header__header3___1b1oq header__header___1zII0 header__snug___lRSNK PriceTrends__priceHeader___fB9X9"
GAS_BUDDY_CLASS_PRICES = "GenericStationListItem__stationListItem___3Jmn4"
GAS_BUDDY_CLASS_STATION = "GenericStationListItem__mainInfoColumn___2kuPq GenericStationListItem__column___2Yqh-"
GAS_BUDDY_CLASS_ST_PRICE = "GenericStationListItem__priceColumn___UmzZ7 GenericStationListItem__column___2Yqh-"

GAS_BUDDY_HTTP_HEADERS = {
    'User-Agent': 'PostmanRuntime/7.19.0',
    'Accept': '*/*',
    'Content-Type': 'text/html'
}

def convert_class_delimiter(el_class, del_from, del_to):
    return del_to.join(el_class.split(del_from))


def get_gas_price_stats(zipcode, grade):
    resp = requests.get(url_gas_buddy % (zipcode, grade), headers=GAS_BUDDY_HTTP_HEADERS)
    pq = PyQuery(resp.content)
    gas_stats_raw = pq('h3.%s' % convert_class_delimiter(GAS_BUDDY_CLASS_STATS, " ", "."))
    print (gas_stats_raw)
    return (gas_stats_raw[0].text, gas_stats_raw[1].text)


def get_gas_prices(zipcode, grade):
    resp = requests.get(url_gas_buddy % (zipcode, grade), headers=GAS_BUDDY_HTTP_HEADERS)
    pq = PyQuery(resp.content)
    gas_prices_raw = pq('div.%s' % convert_class_delimiter(GAS_BUDDY_CLASS_PRICES, " ", "."))
    price_list = []
    for price_obj in gas_prices_raw:
        station_info = {}
        for item in price_obj.getchildren():
            if item.attrib['class'] == GAS_BUDDY_CLASS_STATION:
                #This is the station info
                station_name_raw = item.getchildren()[0].getchildren()
                station_info['Name'] = station_name_raw[0].text
                station_addr_raw = item.getchildren()[2]
                station_info['Address'] = station_addr_raw.text
            elif item.attrib['class'] == GAS_BUDDY_CLASS_ST_PRICE:
                #This is the price
                info_raw = item.getchildren()[0].getchildren()
                if len(info_raw) <= 1:
                    continue
                station_info['Price'] = info_raw[0].text
                station_info['Updated'] = info_raw[1].getchildren()[1].text
        price_list.append(station_info)
    return price_list

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
    grade = config["Gas"]["Grade"]

    gas_price_stats = get_gas_price_stats(zipcode, grade)

    msg = []

    msg.append("주인님,")

    if gas_price_stats is not None:
        msg.append("현재 가솔린 최저가는 %s, 평균가는 %s" % (gas_price_stats[0], gas_price_stats[1]))

    lowest_gas_home = get_gas_prices(zipcode,grade)
    if lowest_gas_home is not None:
        if gas_price_stats is not None:
            msg.append("이고,")
        msg.append("집근처 가솔린 최저가는 %s에서 %s, 주소는 %s" % (lowest_gas_home[0]["Name"], lowest_gas_home[0]["Price"], lowest_gas_home[0]["Address"]))

    if gas_price_stats is not None or lowest_gas_home is not None:
        msg.append("입니다.")
        payload = ' '.join(msg)
        bot.send_message(slack_chatroom_id, "<!here|here>")
        bot.send_message(slack_chatroom_id, payload)
        tbot.send_message(chat_id=telegram_chatroom_id, text=payload)
