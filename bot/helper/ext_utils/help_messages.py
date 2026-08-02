LEECH_HELP_DICT = {
    "main": """<b>Leech Usage</b>

Send a link after the command or reply to a Telegram file/link.

<code>/leech link</code>
<code>/qbleech magnet</code>
<code>/jdleech link</code>
<code>/nzbleech file-or-link</code>

You must set your dump channel from <code>/usetting</code> before starting a task.
All files are uploaded only to that dump channel; Bot PM and custom upload destinations are disabled.""",
    "New-Name": "<b>New name:</b> <code>-n new name</code>",
    "Extract-Zip": "<b>Extract:</b> <code>-e</code> or <code>-e password</code>\n<b>Zip:</b> <code>-z</code> or <code>-z password</code>",
    "Select-Files": "<b>Select torrent/NZB files:</b> <code>-s</code>",
    "Torrent-Seed": "<b>Seed:</b> <code>-d</code> or <code>-d ratio:time</code>",
    "Multi-Link": "<b>Multi:</b> <code>-i number</code>",
    "Bulk": "<b>Bulk:</b> reply to a text file/list and use <code>-b</code>.",
    "Same-Directory": "<b>Same directory:</b> <code>-m folder name</code>",
    "Leech-Type": "<b>Document:</b> <code>-doc</code> | <b>Media:</b> <code>-med</code>",
    "Split-Size": "<b>Split size:</b> <code>-sp 2gb</code>",
    "Thumb": "<b>Thumbnail:</b> <code>-t telegram-photo-link</code>",
    "Force-Start": "<b>Force task:</b> <code>-f</code>, <code>-fd</code> or <code>-fu</code>",
}


def get_bot_commands():
    commands = {
        "Leech": "[link/file] Leech to your dump channel",
        "QbLeech": "[magnet/torrent] Leech using qBittorrent",
        "JdLeech": "[link/file] Leech using JDownloader",
        "NzbLeech": "[nzb] Leech using SABnzbd",
        "CancelTask": "[gid/reply] Cancel a task",
        "CancelAll": "Cancel all tasks",
        "ForceStart": "[gid/reply] Force-start a queued task",
        "Select": "[gid/reply] Select torrent/NZB files",
        "Status": "Show active tasks",
        "Stats": "Show bot and system statistics",
        "MediaInfo": "[reply/link] Show media information",
        "UserSet": "Set or change your dump channel",
        "Ping": "Check bot response time",
        "Help": "Show command help",
        "Authorize": "[SUDO] Authorize a chat or user",
        "UnAuthorize": "[SUDO] Remove authorization",
        "AddSudo": "[OWNER] Add a sudo user",
        "RmSudo": "[OWNER] Remove a sudo user",
        "BlackList": "[SUDO] Blacklist a user",
        "RmBlackList": "[SUDO] Remove a blacklist entry",
        "Users": "[SUDO] Show saved dump channels",
        "BotSet": "[SUDO] Bot settings",
        "Broadcast": "[SUDO] Broadcast a message",
        "Restart": "[SUDO] Restart the bot",
        "RestartSessions": "[SUDO] Restart Telegram sessions",
        "Log": "[SUDO] Get bot logs",
        "GenPyroSess": "[SUDO] Generate a Pyrogram session",
        "AddImage": "Add a bot image",
        "Images": "Manage bot images",
        "Shell": "[OWNER] Run a shell command",
        "AExec": "[OWNER] Execute async Python",
        "Exec": "[OWNER] Execute Python",
        "ClearLocals": "[OWNER] Clear execution locals",
    }
    return commands


BOT_COMMANDS = get_bot_commands()


def get_help_string():
    from ..telegram_helper.bot_commands import BotCommands

    lines = [
        "<b>Leech-only Bot Commands</b>",
        "",
        "Set your dump channel first with <code>/usetting</code>.",
        "",
    ]
    for key in BotCommands.get_commands():
        command = getattr(BotCommands, f"{key}Command", None)
        if not command:
            continue
        if isinstance(command, list):
            command_text = " / ".join(f"/{item}" for item in command)
        else:
            command_text = f"/{command}"
        description = BOT_COMMANDS.get(key, "Bot command")
        lines.append(f"{command_text} — {description}")
    return "\n".join(lines)


help_string = get_help_string()
