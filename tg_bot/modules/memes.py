import random, re, os, io, asyncio
from PIL import Image
from io import BytesIO
from telegram import Message, Update, Bot, User
from telegram import MessageEntity
from telegram.ext import Filters, MessageHandler, run_async
from deeppyer import deepfry

from tg_bot import dispatcher
from tg_bot.modules.disable import DisableAbleCommandHandler

re
# D A N K module by @deletescape - based on https://github.com/wrxck/mattata/blob/master/plugins/copypasta.mattata

@run_async
def copypasta(bot: Bot, update: Update):
    message = update.effective_message
    emojis = ["😂", "😭", "😡", "😂", "👌", "✌", "💞", "👍", "👌", "💯", "🎶", "👀", "😂", "👓", "👏", "👐", "🍕", "💥", "🍴", "💦", "💦", "🍑", "🍆", "😩", "😏", "👉👌", "👀", "👅", "😩", "🚰"]
    reply_text = random.choice(emojis)
    b_char = random.choice(message.reply_to_message.text).lower() # choose a random character in the message to be substituted with 🅱️
    for c in message.reply_to_message.text:
        if c == " ":
            reply_text += random.choice(emojis)
        elif c in emojis:
            reply_text += c
            reply_text += random.choice(emojis)
        elif c.lower() == b_char:
            reply_text += "🅱️"
        else:
            if bool(random.getrandbits(1)):
                reply_text += c.upper()
            else:
                reply_text += c.lower()
    reply_text += random.choice(emojis)
    message.reply_to_message.reply_text(reply_text)

# only use one event loop for the stupid face recognition
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# D A N K module by @deletescape

@run_async
def bmoji(bot: Bot, update: Update): #🅱️
    message = update.effective_message
    reply_text = re.sub(r'(r|R)', "🅱️", message.reply_to_message.text)
    reply_text = re.sub(r'(p|P)', "🅱️", reply_text)
    reply_text = re.sub(r'(n|N)', "🅱️", reply_text)
    message.reply_to_message.reply_text(reply_text)

@run_async
def clapmoji(bot: Bot, update: Update):
    message = update.effective_message
    reply_text = "👏 "
    for i in message.reply_to_message.text:
        if i == " ":
            reply_text += " 👏 "
        else:
            reply_text += i
    reply_text += " 👏"
    message.reply_to_message.reply_text(reply_text)
    
@run_async
def angrymoji(bot: Bot, update: Update):
    message = update.effective_message
    reply_text = "😡 "
    for i in message.reply_to_message.text:
        if i == " ":
            reply_text += " 😡 "
        else:
            reply_text += i
    reply_text += " 😡"
    message.reply_to_message.reply_text(reply_text)

@run_async
def crymoji(bot: Bot, update: Update):
    message = update.effective_message
    reply_text = "😭 "
    for i in message.reply_to_message.text:
        if i == " ":
            reply_text += " 😭 "
        else:
            reply_text += i
    reply_text += " 😭"
    message.reply_to_message.reply_text(reply_text)
    
    
@run_async
def owo(bot: Bot, update: Update):
    message = update.effective_message
    faces = ['(・`ω´・)',';;w;;','owo','UwU','>w<','^w^','\(^o\) (/o^)/','( ^ _ ^)∠☆','(ô_ô)','~:o',';-;', '(*^*)', '(>_', '(♥_♥)', '*(^O^)*', '((+_+))']
    reply_text = re.sub(r'(r|l)', "w", message.reply_to_message.text)
    reply_text = re.sub(r'(R|L)', 'W', reply_text)
    reply_text = re.sub(r'n([aeiou])', r'ny\1', reply_text)
    reply_text = re.sub(r'N([aeiouAEIOU])', r'Ny\1', reply_text)
    reply_text = re.sub(r'\!+', ' ' + random.choice(faces), reply_text)
    reply_text = reply_text.replace("ove", "uv")
    reply_text += ' ' + random.choice(faces)
    message.reply_to_message.reply_text(reply_text)

@run_async
def deepfryer(bot: Bot, update: Update):
    message = update.effective_message
    if message.reply_to_message:
        data = message.reply_to_message.photo
    else:
        data = []
     # check if message does contain a photo and cancel when not
    if not data:
        message.reply_text("What am I supposed to do with this?!")
        return
     # download last photo (highres) as byte array
    photodata = data[len(data) - 1].get_file().download_as_bytearray()
    image = Image.open(io.BytesIO(photodata))
     # the following needs to be executed async (because dumb lib)
    global loop
    loop.run_until_complete(process_deepfry(image, message.reply_to_message, bot))
 async def process_deepfry(image: Image, reply: Message, bot: Bot):
    # DEEPFRY IT
    image = await deepfry(
        img=image,
        token=os.getenv('DEEPFRY_TOKEN', ''),
        url_base='westeurope'
    )
     bio = BytesIO()
    bio.name = 'image.jpeg'
    image.save(bio, 'JPEG')
    bio.seek(0)
     # send it back
    reply.reply_photo(bio)

__help__ = "many memz"  # no help string

__mod_name__ = "Memes"

COPYPASTA_HANDLER = DisableAbleCommandHandler("copypasta", copypasta)
COPYPASTA_ALIAS_HANDLER = DisableAbleCommandHandler("😂", copypasta)
CLAPMOJI_HANDLER = DisableAbleCommandHandler("clapmoji", clapmoji)
CLAPMOJI_ALIAS_HANDLER = DisableAbleCommandHandler("👏", clapmoji)
ANGRYMOJI_HANDLER = DisableAbleCommandHandler("angrymoji", angrymoji)
ANGRYMOJI_ALIAS_HANDLER = DisableAbleCommandHandler("😡", angrymoji)
CRYMOJI_HANDLER = DisableAbleCommandHandler("crymoji", crymoji)
CRYMOJI_ALIAS_HANDLER = DisableAbleCommandHandler("😭", crymoji)
BMOJI_HANDLER = DisableAbleCommandHandler("🅱️", bmoji)
BMOJI_ALIAS_HANDLER = DisableAbleCommandHandler("bmoji", bmoji)
OWO_HANDLER = DisableAbleCommandHandler("owo", owo)
DEEPFRY_HANDLER = DisableAbleCommandHandler("deepfry", deepfryer, admin_ok=True)


dispatcher.add_handler(COPYPASTA_HANDLER)
dispatcher.add_handler(COPYPASTA_ALIAS_HANDLER)
dispatcher.add_handler(CLAPMOJI_HANDLER)
dispatcher.add_handler(CLAPMOJI_ALIAS_HANDLER)
dispatcher.add_handler(ANGRYMOJI_HANDLER)
dispatcher.add_handler(ANGRYMOJI_ALIAS_HANDLER)
dispatcher.add_handler(CRYMOJI_HANDLER)
dispatcher.add_handler(CRYMOJI_ALIAS_HANDLER)
dispatcher.add_handler(BMOJI_HANDLER)
dispatcher.add_handler(BMOJI_ALIAS_HANDLER)
dispatcher.add_handler(OWO_HANDLER)
dispatcher.add_handler(DEEPFRY_HANDLER) 

