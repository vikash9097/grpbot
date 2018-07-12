import logging
import os
import sys

import telegram.ext as tg

from telegram.error import Unauthorized, InvalidToken, RetryAfter, TimedOut

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error("You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting.")
    quit(1)

ENV = bool(os.environ.get('ENV', False))

if ENV:
    TOKEN = os.environ.get('TOKEN', None)
    try:
        OWNER_ID = int(os.environ.get('OWNER_ID', None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    MESSAGE_DUMP = os.environ.get('MESSAGE_DUMP', None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

    try:
        SUDO_USERS = set(int(x) for x in os.environ.get("SUDO_USERS", "").split())
    except ValueError:
        raise Exception("Your sudo users list does not contain valid integers.")

    try:
        SUPPORT_USERS = set(int(x) for x in os.environ.get("SUPPORT_USERS", "").split())
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        WHITELIST_USERS = set(int(x) for x in os.environ.get("WHITELIST_USERS", "").split())
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

    WEBHOOK = bool(os.environ.get('WEBHOOK', False))
    URL = os.environ.get('URL', "")  # Does not contain token
    PORT = int(os.environ.get('PORT', 5000))
    CERT_PATH = os.environ.get("CERT_PATH")

    DB_URI = os.environ.get('DATABASE_URL')
    DONATION_LINK = os.environ.get('DONATION_LINK')
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()
    DEL_CMDS = bool(os.environ.get('DEL_CMDS', False))
    STRICT_GBAN = bool(os.environ.get('STRICT_GBAN', False))
    WORKERS = int(os.environ.get('WORKERS', 8))
    BAN_STICKER = os.environ.get('BAN_STICKER', 'CAADBAADoxMAAnrRWwZY0Xxza446JgI')
    ALLOW_EXCL = os.environ.get('ALLOW_EXCL', False)
    STRICT_GMUTE = bool(os.environ.get('STRICT_GMUTE', False))

else:
    from tg_bot.config import Development as Config
    TOKEN = Config.API_KEY
    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")

    MESSAGE_DUMP = Config.MESSAGE_DUMP
    OWNER_USERNAME = Config.OWNER_USERNAME

    try:
        SUDO_USERS = set(int(x) for x in Config.SUDO_USERS or [])
    except ValueError:
        raise Exception("Your sudo users list does not contain valid integers.")

    try:
        SUPPORT_USERS = set(int(x) for x in Config.SUPPORT_USERS or [])
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        WHITELIST_USERS = set(int(x) for x in Config.WHITELIST_USERS or [])
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH

    DB_URI = Config.SQLALCHEMY_DATABASE_URI
    DONATION_LINK = Config.DONATION_LINK
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    DEL_CMDS = Config.DEL_CMDS
    STRICT_GBAN = Config.STRICT_GBAN
    WORKERS = Config.WORKERS
    BAN_STICKER = Config.BAN_STICKER
    ALLOW_EXCL = Config.ALLOW_EXCL
    STRICT_GMUTE = Config.STRICT_GMUTE

SUDO_USERS.add(OWNER_ID)

updater = tg.Updater(TOKEN, workers=WORKERS)

dispatcher = updater.dispatcher

SUDO_USERS = list(SUDO_USERS)
WHITELIST_USERS = list(WHITELIST_USERS)
SUPPORT_USERS = list(SUPPORT_USERS)

# Load at end to ensure all prev variables have been set
from tg_bot.modules.helper_funcs.handlers import CustomCommandHandler, CustomRegexHandler

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler

if ALLOW_EXCL:
    tg.CommandHandler = CustomCommandHandler

def _start_polling(self, poll_interval, timeout, read_latency, bootstrap_retries, clean,
                        allowed_updates):  # pragma: no cover
# Thread target of thread 'updater'. Runs in background, pulls
         # updates from Telegram and inserts them in the update queue of the
         # Dispatcher.
cur_interval = poll_interval
         self.logger.debug('Updater thread started')
 
         self._bootstrap(bootstrap_retries, clean=clean, webhook_url='', allowed_updates=None)
 
         while self.running:
             try:
                 updates = self.bot.get_updates(
                     self.last_update_id,
                     timeout=timeout,
                     read_latency=read_latency,
                     allowed_updates=allowed_updates)
             except RetryAfter as e:
                 self.logger.info(str(e))
                 cur_interval = 0.5 + e.retry_after
            except TimedOut as toe:
                self.logger.debug('Timed out getting Updates: %s', toe)
                # If get_updates() failed due to timeout, we should retry asap.
                cur_interval = 0
             except TelegramError as te:
		self.logger.error('Error while getting Updates: %s', te)
 # Put the error into the update queue and let the Dispatcher
                 # broadcast it
                 self.update_queue.put(te)
 
                 cur_interval = self._increase_poll_interval(cur_interval)
             else:
                 if not self.running:
                     if len(updates) > 0:
                         self.logger.debug('Updates ignored and will be pulled '
                                           'again on restart.')
                     break
 
                 if updates:
                     for update in updates:
                         self.update_queue.put(update)
                     self.last_update_id = updates[-1].update_id + 1
 
                 cur_interval = poll_interval
 if cur_interval:
                sleep(cur_interval)
 
