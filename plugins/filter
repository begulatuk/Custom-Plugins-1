""" setup filters """

# Copyright (C) 2020-2021 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

import re
import asyncio
from typing import Dict

from userge import userge, Message, filters, get_collection

FILTERS_COLLECTION = get_collection("filters")
CHANNEL = userge.getCLogger(__name__)

FILTERS_DATA: Dict[int, Dict[str, int]] = {}
FILTERS_CHATS = filters.create(lambda _, __, query: query.chat and query.chat.id in FILTERS_DATA)

_SUPPORTED_TYPES = (":audio:", ":video:", ":photo:", ":document:",
                    ":sticker:", ":animation:", ":voice:", ":video_note:",
                    ":media:", ":game:", ":contact:", ":location:",
                    ":venue:", ":web_page:", ":poll:", ":via_bot:",
                    ":forward_date:", ":mentioned:", ":service:",
                    ":media_group_id:", ":game_high_score:", ":pinned_message:",
                    ":new_chat_title:", ":new_chat_photo:", ":delete_chat_photo:")




@userge.on_filters(~filters.edited & FILTERS_CHATS, group=1)
async def chat_filter(message: Message) -> None:
    """ filter handler """
    if not message.from_user:
        return
    try:
        for name in FILTERS_DATA[message.chat.id]:
            reply = False
            if name.startswith(':') and name.endswith(':'):
                media_type = name.strip(':')
                if getattr(message, media_type, None):
                    await asyncio.sleep(5)
                    reply = True
            elif message.text:
                l_name = name.lower()
                input_text = message.text.strip().lower()
                filter_text = re.search(l_name, input_text)
                
                if (input_text == l_name
                        or input_text.startswith(f"{l_name} ")
                        or input_text.endswith(f" {l_name}")
                        or filter_text is not None
                        or f" {l_name} " in input_text):
                    await asyncio.sleep(3)
                    reply = True
            if reply:
                await CHANNEL.forward_stored(client=message.client,
                                             message_id=FILTERS_DATA[message.chat.id][name],
                                             chat_id=message.chat.id,
                                             user_id=message.from_user.id,
                                             reply_to_message_id=message.message_id)
    except RuntimeError:
        pass
