import html
from telegram import Message, Update, Bot, User, Chat, ParseMode
from telegram.error import BadRequest, TelegramError
from telegram.ext import run_async, CommandHandler, MessageHandler, Filters
from telegram.utils.helpers import mention_html
from tg_bot import dispatcher, OWNER_ID, SUDO_USERS
import tg_bot.modules.sql.users_sql as sql
from tg_bot.modules.helper_funcs.filters import CustomFilters

@run_async
def listsudo(bot: Bot, update: Update):
    message = update.effective_message
    reply_msg = "**SUDO USERS:**"
    for i in SUDO_USERS:
       reply_msg += "\n" + str(i)

    message.reply_text(reply_msg)
    return

__mod_name__ = "Sudo users"
SUDOUSER_HANDLER = CommandHandler("listsudo", listsudo, filters=CustomFilters.sudo_filter)
dispatcher.add_handler(SUDOUSER_HANDLER)
