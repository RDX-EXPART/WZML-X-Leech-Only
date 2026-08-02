from asyncio import sleep
from functools import partial
from io import BytesIO

from pyrogram.enums import ButtonStyle, ChatType
from pyrogram.filters import create
from pyrogram.handlers import MessageHandler

from .. import auth_chats, sudo_users, user_data
from ..core.tg_client import TgClient
from ..helper.ext_utils.bot_utils import new_task, update_user_ldata
from ..helper.ext_utils.db_handler import database
from ..helper.telegram_helper.button_build import ButtonMaker
from ..helper.telegram_helper.message_utils import (
    delete_message,
    edit_message,
    send_file,
    send_message,
)

handler_dict = {}

DUMP_PROMPT = """<b>Set Dump Channel</b>

1. Add this bot as an administrator in your channel.
2. Send the channel ID or public @username here.
3. For a forum topic, use: <code>-1001234567890|123</code>

Private messages and <code>pm</code> are not allowed.
┖ <b>Time Left:</b> <code>60 sec</code>"""


def _dump_value(user_id):
    return user_data.get(user_id, {}).get("LEECH_DUMP_CHAT")


async def get_user_settings(from_user, stype="leech"):
    user_id = from_user.id
    dump_chat = _dump_value(user_id)
    buttons = ButtonMaker()
    buttons.data_button(
        "Change Dump" if dump_chat else "Set Dump",
        f"userset {user_id} setdump",
        style=ButtonStyle.PRIMARY,
    )
    buttons.data_button(
        "Close",
        f"userset {user_id} close",
        position="footer",
        style=ButtonStyle.DANGER,
    )
    status = f"<code>{dump_chat}</code>" if dump_chat else "<b>Not Set</b>"
    text = f"""⌬ <b>Leech Settings</b>
│
├ <b>User</b> → {from_user.mention(style="html")}
├ <b>Dump Channel</b> → {status}
└ <b>Bot PM</b> → <b>Disabled</b>

<i>A dump channel is required before you can start any leech task.</i>"""
    return text, buttons.build_menu(1)


async def update_user_settings(query):
    text, buttons = await get_user_settings(query.from_user)
    await edit_message(query.message, text, buttons)


async def event_handler(client, query, pfunc, rfunc):
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    handler_dict[user_id] = True

    async def event_filter(_, __, event):
        user = event.from_user or event.sender_chat
        return bool(
            user
            and user.id == user_id
            and event.chat.id == chat_id
            and event.text
        )

    handler = client.add_handler(
        MessageHandler(pfunc, filters=create(event_filter)), group=-1
    )
    elapsed = 0.0
    while handler_dict.get(user_id) and elapsed < 60:
        await sleep(0.5)
        elapsed += 0.5
    timed_out = handler_dict.get(user_id, False)
    handler_dict[user_id] = False
    client.remove_handler(*handler)
    if timed_out:
        await rfunc()


def _parse_dump_input(value):
    value = value.strip()
    if not value or value.casefold() == "pm":
        raise ValueError("Private messages are not allowed. Please send a channel ID or @username.")
    if value.startswith(("b:", "u:", "h:")):
        value = value[2:]
    chat_ref, separator, topic = value.partition("|")
    chat_ref = chat_ref.strip()
    if not chat_ref:
        raise ValueError("Please send a valid channel ID or @username.")
    if chat_ref.lstrip("-").isdigit():
        chat_ref = int(chat_ref)
    if separator:
        topic = topic.strip()
        if not topic.isdigit() or int(topic) <= 0:
            raise ValueError("Topic ID must be a positive number.")
        topic = int(topic)
    else:
        topic = None
    return chat_ref, topic


@new_task
async def set_dump_channel(_, message, rfunc):
    user_id = message.from_user.id
    handler_dict[user_id] = False
    try:
        chat_ref, topic_id = _parse_dump_input(message.text)
        chat = await TgClient.bot.get_chat(chat_ref)
        if chat.type not in {
            ChatType.CHANNEL,
            ChatType.SUPERGROUP,
            ChatType.GROUP,
            ChatType.FORUM,
        }:
            raise ValueError("The dump destination must be a channel or group.")

        member = await TgClient.bot.get_chat_member(chat.id, TgClient.bot.me.id)
        privileges = getattr(member, "privileges", None)
        if privileges is None:
            raise ValueError("Make the bot an administrator in the dump channel first.")
        if chat.type == ChatType.CHANNEL and not getattr(
            privileges, "can_post_messages", False
        ):
            raise ValueError("Give the bot permission to post messages in the channel.")
        if not getattr(privileges, "can_delete_messages", False):
            raise ValueError("Give the bot permission to delete messages in the dump channel.")

        dump_value = f"{chat.id}|{topic_id}" if topic_id else chat.id
        update_user_ldata(user_id, "LEECH_DUMP_CHAT", dump_value)
        await database.update_user_data(user_id)
        await send_message(
            message,
            f"✅ <b>Dump channel saved:</b> <code>{dump_value}</code>",
        )
        await delete_message(message)
    except Exception as error:
        await send_message(message, f"❌ <b>Could not set dump channel:</b> {error}")
    await rfunc()


@new_task
async def edit_user_settings(client, query):
    data = query.data.split()
    if len(data) < 3:
        return await query.answer()
    user_id = query.from_user.id
    if user_id != int(data[1]):
        return await query.answer("Not Yours!", show_alert=True)

    handler_dict[user_id] = False
    action = data[2]
    if action in {"leech", "back"}:
        await query.answer()
        await update_user_settings(query)
    elif action == "setdump":
        await query.answer()
        buttons = ButtonMaker()
        buttons.data_button("Stop", f"userset {user_id} leech")
        buttons.data_button(
            "Close",
            f"userset {user_id} close",
            position="footer",
            style=ButtonStyle.DANGER,
        )
        await edit_message(query.message, DUMP_PROMPT, buttons.build_menu(1))
        rfunc = partial(update_user_settings, query)
        pfunc = partial(set_dump_channel, rfunc=rfunc)
        await event_handler(client, query, pfunc, rfunc)
    else:
        await query.answer()
        await delete_message(query.message)


@new_task
async def send_user_settings(_, message):
    text, buttons = await get_user_settings(message.from_user)
    await send_message(message, text, buttons)


@new_task
async def get_users_settings(_, message):
    lines = []
    if auth_chats:
        lines.append(f"AUTHORIZED_CHATS: {auth_chats}")
    if sudo_users:
        lines.append(f"SUDO_USERS: {sudo_users}")
    for user_id, data in user_data.items():
        if dump_chat := data.get("LEECH_DUMP_CHAT"):
            lines.append(f"{user_id}: LEECH_DUMP_CHAT = {dump_chat}")
    if not lines:
        return await send_message(message, "No user dump channels have been set.")
    output = "\n".join(lines)
    if len(output.encode()) > 4000:
        with BytesIO(output.encode()) as file:
            file.name = "users_settings.txt"
            await send_file(message, file)
    else:
        await send_message(message, output)
