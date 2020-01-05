#!/usr/local/bin/python

import re, requests
from datetime import datetime
from babel import Locale

import sys

import TelegramBot

from utils.configmanager import ConfigManager

"""
====================== Main ===========================
"""
if __name__ == "__main__":
    if (len(sys.argv) <= 1):
        print("This program requires filepath to the video.")
        quit(1)
    path_to_video = sys.argv[1]
    config = ConfigManager("settings.conf").parse()

    tbot = TelegramBot.TelegramBot(token=config["Telegram"]["Token"])
    telegram_chatroom_id = config["Telegram"]["ChatroomID"]

    tbot.send_message(telegram_chatroom_id, "주인님, 차고에 움직임을 감지했습니다. 캡쳐 영상을 확인하여 주시기 바랍니다.")

    telegram_video = tbot.send_video(telegram_chatroom_id, path_to_video)
