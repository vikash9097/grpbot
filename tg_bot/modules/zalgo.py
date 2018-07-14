from telegram import ChatAction
import html
import re
import json
from datetime import datetime
from typing import Optional, List
import time
import requests
from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters
from telegram.utils.helpers import escape_markdown, mention_html
from tg_bot import dispatcher
from tg_bot.modules.disable import DisableAbleCommandHandler
from zalgo_text import zalgo    

def zal(bot: Bot, update: Update, args):
    current_time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
    if update.message.reply_to_message is not None:
        args = update.message.reply_to_message.text
        args = args.split(" ")
    input_text = " ".join(args).lower()
    if input_text == "":
        update.message.reply_text("Type in some text Madarchod!")
        return
    zalgofied_text = zalgo.zalgo().zalgofy(input_text)
    update.message.reply_text(zalgofied_text)

dispatcher.add_handler(DisableAbleCommandHandler('zal', zal, pass_args=True))