""" Fun Stickers for Tweet """

# By @Krishna_Singhal

import os
import requests

from PIL import Image
from validators.url import url

from userge.utils import demojify
from userge import userge, Config, Message

_LOG = logging.getLogger(__name__)

CONVERTED_IMG = Config.DOWN_PATH + "img.png"


@userge.on_cmd("jokowi", about={
    'header': "Custom Sticker of Trump Tweet",
    'usage': "{tr}trump [text | reply to text]"})
async def jokowi_tweet(msg: Message):
    """ Fun sticker of Trump Tweet """
    replied = msg.reply_to_message
    text = msg.input_str
    if replied and not text:
        text = replied.text
    if not text:
        await msg.err("Trump Need some Text for Tweet 🙄")
        return
    await msg.edit("```Requesting trump to tweet... 😃```")
    await _tweets(msg, text, type_="jokowitweet")
    _LOG.info(text, msg)




async def _tweets(msg: Message, text: str, username: str = '', type_: str = "tweet") -> None:
    api_url = f"https://nekobot.xyz/api/imagegen?type={type_}&text={demojify(text)}"
    if username:
        api_url += f"&username={demojify(username)}"
    res = requests.get(api_url).json()
    tweets_ = res.get("message")
    if not url(tweets_):
        await msg.err("Invalid Syntax, Exiting...")
        return
    tmp_file = Config.DOWN_PATH + "temp.png"
    with open(tmp_file, "wb") as t_f:
        t_f.write(requests.get(tweets_).content)
    img = Image.open(tmp_file)
    img.save(CONVERTED_IMG)
    await msg.delete()
    msg_id = msg.reply_to_message.message_id if msg.reply_to_message else None
    await msg.client.send_photo(chat_id=msg.chat.id,
                                photo=CONVERTED_IMG,
                                reply_to_message_id=msg_id)
    os.remove(tmp_file)
    os.remove(CONVERTED_IMG)
