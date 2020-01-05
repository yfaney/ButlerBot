#!/usr/local/bin/python3

import sys

import TelegramBot

from utils.configmanager import ConfigManager

"""
====================== Main ===========================
"""
if __name__ == "__main__":
    if (len(sys.argv) <= 1):
        print("This program requires an argument for the battery percentage")
        quit(1)
    batt = int(sys.argv[1])
    config = ConfigManager("settings.conf").parse()

    tbot = TelegramBot.TelegramBot(token=config["Telegram"]["Token"])
    telegram_chatroom_id = config["Telegram"]["ChatroomID"]

    if batt < 20:
        tbot.send_message(telegram_chatroom_id, "주인님, 맥북 배터리 잔량이 20% 이하입니다. 충전기를 연결해 주십시오.")
    elif batt > 80:
        tbot.send_message(telegram_chatroom_id, "주인님, 맥북 배터리가 80% 이상 충전되었습니다. 배터리 수명을 위해 충전기를 분리해 주십시오.")
