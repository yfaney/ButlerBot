#!/usr/local/bin/python

import re, requests
from pyquery import PyQuery
from datetime import datetime
from babel import Locale

import sys

import SlackBot

from utils.configmanager import ConfigManager

url_gas_buddy = "https://www.gasbuddy.com/home?search=%s&fuel=%s"

GAS_BUDDY_CLASS_STATS = "style__header3___3T2tm style__header___onURp style__snug___2HJ4K styles__priceHeader___38ONR"
GAS_BUDDY_CLASS_PRICES = "styles__stationListItem___xKFP_"
GAS_BUDDY_CLASS_STATION = "styles__mainInfoColumn___1KXCl styles__column___x6UAG"
GAS_BUDDY_CLASS_ST_PRICE = "styles__priceColumn___33js5 styles__column___x6UAG"

def convert_class_delimiter(el_class, del_from, del_to):
    return del_to.join(el_class.split(del_from))


def get_gas_price_stats(zipcode, grade):
    resp = requests.get(url_gas_buddy % (zipcode, grade))
    pq = PyQuery(resp.content)
    gas_stats_raw = pq('h3.%s' % convert_class_delimiter(GAS_BUDDY_CLASS_STATS, " ", "."))
    print (gas_stats_raw)
    return (gas_stats_raw[0].text, gas_stats_raw[1].text)


def get_gas_prices(zipcode, grade):
    resp = requests.get(url_gas_buddy % (zipcode, grade))
    pq = PyQuery(resp.content)
    gas_prices_raw = pq('div.%s' % convert_class_delimiter(GAS_BUDDY_CLASS_PRICES, " ", "."))
    price_list = []
    for price_obj in gas_prices_raw:
        station_info = {}
        for item in price_obj.getchildren():
            if item.attrib['class'] == GAS_BUDDY_CLASS_STATION:
                #This is the station info
                info_raw = item.getchildren()[0].getchildren()
                station_info['Name'] = info_raw[0].text
                station_info['Address'] = info_raw[2].text
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
    slack_chatroom_id = config["Slack"]["ChatroomID"]
    zipcode = config["Location"]["zipcode"]
    grade = config["Gas"]["Grade"]

    gas_price_stats = get_gas_price_stats(zipcode, grade)

    if gas_price_stats is not None:
        bot.send_message(slack_chatroom_id, "<!here|here>")
        bot.send_message(slack_chatroom_id, "주인님, 현재 가솔린 최저가는 %s, 평균가는 %s입니다." % (gas_price_stats[0], gas_price_stats[1]))
