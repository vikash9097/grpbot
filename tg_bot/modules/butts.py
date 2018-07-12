from telegram import ChatAction
from gtts import gTTS
import html
import urllib.request
from PyLyrics import *
import wget
import re
import json
import random
from random import randint
from datetime import datetime
from typing import Optional, List
import pyowm
import time
import os
import urllib
from urllib.request import urlopen, urlretrieve
from urllib.parse import quote_plus, urlencode
import requests
from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters
from telegram.utils.helpers import escape_markdown, mention_html
#import urbandictionary as ud
from tg_bot import dispatcher, OWNER_ID, SUDO_USERS, SUPPORT_USERS, WHITELIST_USERS, BAN_STICKER
from tg_bot.__main__ import STATS, USER_INFO
from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot.modules.helper_funcs.extraction import extract_user
from tg_bot.modules.helper_funcs.filters import CustomFilters

def butts(bot: Bot, update: Update):
    nsfw = requests.get('http://api.obutts.ru/noise/1').json()[0]["preview"]
    final = "http://media.obutts.ru/{}".format(nsfw)
    update.message.reply_photo(final)
		
__help__ = """
 - /boobs: Sends Random Boobs pic.
 - /butts: Sends Random Butts pic.
"""
__mod_name__ = "NSFW"
dispatcher.add_handler(CommandHandler('butts', butts))