import html
from telegram import Message, Update, Bot, User, Chat, ParseMode
from telegram.error import BadRequest, TelegramError
from telegram.ext import run_async, CommandHandler, MessageHandler, Filters
from telegram.utils.helpers import mention_html
from tg_bot import dispatcher, OWNER_ID, SUPPORT_USERS
import tg_bot.modules.sql.users_sql as sql
from tg_bot.modules.helper_funcs.filters import CustomFilters

@run_async
def listsupport(bot: Bot, update: Update):
    message = update.effective_message
    reply_msg = "**SUPPORT USERS:**"
    for i in SUPPORT_USERS:
       reply_msg += "\n" + str(i)

    message.reply_text(reply_msg)
    return

__mod_name__ = "Support users"
SUPPORTUSER_HANDLER = CommandHandler("listsupport", listsupport, filters=CustomFilters.sudo_filter)
dispatcher.add_handler(SUPPORTUSER_HANDLER)
