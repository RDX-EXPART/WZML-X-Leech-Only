from ..helper.ext_utils.bot_utils import COMMAND_USAGE, new_task
from ..helper.ext_utils.help_messages import LEECH_HELP_DICT, help_string
from ..helper.telegram_helper.button_build import ButtonMaker
from ..helper.telegram_helper.message_utils import (
    delete_message,
    edit_message,
    send_message,
)


@new_task
async def arg_usage(_, query):
    data = query.data.split()
    message = query.message
    await query.answer()
    if data[1] == "close":
        return await delete_message(message, message.reply_to_message)

    page = int(data[3])
    if data[1] in ("nex", "pre", "back"):
        pages = COMMAND_USAGE.get("leech")
        button_index = page + 1
        if pages and 1 <= button_index < len(pages):
            await edit_message(message, pages[0], pages[button_index])
    elif data[1] == "leech":
        buttons = ButtonMaker()
        buttons.data_button("Back", f"help back leech {page}")
        await edit_message(
            message, LEECH_HELP_DICT[data[2]], buttons.build_menu(1)
        )


@new_task
async def bot_help(_, message):
    await send_message(message, help_string)
