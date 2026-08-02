# ruff: noqa: F403, F405

from pyrogram.filters import command, regex
from pyrogram.handlers import CallbackQueryHandler, EditedMessageHandler, MessageHandler
from pyrogram.types import BotCommand

from ..core.config_manager import Config
from ..helper.ext_utils.help_messages import BOT_COMMANDS
from ..helper.telegram_helper.bot_commands import BotCommands
from ..helper.telegram_helper.filters import CustomFilters
from ..modules import *
from .tg_client import TgClient


async def add_handlers():
    bot = TgClient.bot

    # Access and owner tools.
    for callback, cmd, access_filter in [
        (authorize, BotCommands.AuthorizeCommand, CustomFilters.sudo),
        (unauthorize, BotCommands.UnAuthorizeCommand, CustomFilters.sudo),
        (add_sudo, BotCommands.AddSudoCommand, CustomFilters.sudo),
        (remove_sudo, BotCommands.RmSudoCommand, CustomFilters.sudo),
        (add_blacklist, BotCommands.BlackListCommand, CustomFilters.sudo),
        (remove_blacklist, BotCommands.RmBlackListCommand, CustomFilters.sudo),
        (send_bot_settings, BotCommands.BotSetCommand, CustomFilters.sudo),
        (broadcast, BotCommands.BroadcastCommand, CustomFilters.sudo),
        (aioexecute, BotCommands.AExecCommand, CustomFilters.sudo),
        (execute, BotCommands.ExecCommand, CustomFilters.sudo),
        (clear, BotCommands.ClearLocalsCommand, CustomFilters.sudo),
        (log, BotCommands.LogCommand, CustomFilters.sudo),
        (restart_bot, BotCommands.RestartCommand, CustomFilters.sudo),
        (restart_sessions, BotCommands.RestartSessionsCommand, CustomFilters.sudo),
        (gen_pyro_string, BotCommands.GenPyroSessCommand, CustomFilters.sudo),
        (get_users_settings, BotCommands.UsersCommand, CustomFilters.sudo),
    ]:
        bot.add_handler(
            MessageHandler(
                callback,
                filters=command(cmd, case_sensitive=True) & access_filter,
            )
        )

    bot.add_handler(
        MessageHandler(
            black_listed,
            filters=regex(r"^/") & CustomFilters.authorized & CustomFilters.blacklisted,
        )
    )
    bot.add_handler(
        MessageHandler(
            run_shell,
            filters=command(BotCommands.ShellCommand, case_sensitive=True)
            & CustomFilters.sudo,
        )
    )
    bot.add_handler(
        EditedMessageHandler(
            run_shell,
            filters=command(BotCommands.ShellCommand, case_sensitive=True)
            & CustomFilters.owner,
        )
    )

    # Leech-only transfer entry points.
    for callback, cmd in [
        (leech, BotCommands.LeechCommand),
        (qb_leech, BotCommands.QbLeechCommand),
        (jd_leech, BotCommands.JdLeechCommand),
        (nzb_leech, BotCommands.NzbLeechCommand),
    ]:
        bot.add_handler(
            MessageHandler(
                callback,
                filters=command(cmd, case_sensitive=True) & CustomFilters.authorized,
            )
        )

    # Task controls and useful leech utilities.
    bot.add_handler(
        MessageHandler(
            cancel,
            filters=regex(rf"^/{BotCommands.CancelTaskCommand[1]}?(?:_\w+).*$")
            & CustomFilters.authorized,
        )
    )
    for callback, cmd in [
        (cancel_all_buttons, BotCommands.CancelAllCommand),
        (remove_from_queue, BotCommands.ForceStartCommand),
        (mediainfo, BotCommands.MediaInfoCommand),
        (ping, BotCommands.PingCommand),
        (bot_help, BotCommands.HelpCommand),
        (bot_stats, BotCommands.StatsCommand),
        (task_status, BotCommands.StatusCommand),
        (picture_add, BotCommands.AddImageCommand),
        (pictures, BotCommands.ImagesCommand),
    ]:
        bot.add_handler(
            MessageHandler(
                callback,
                filters=command(cmd, case_sensitive=True) & CustomFilters.authorized,
            )
        )
    bot.add_handler(
        MessageHandler(
            select,
            filters=regex(rf"^/{BotCommands.SelectCommand[1]}?(?:_\w+).*$")
            & CustomFilters.authorized,
        )
    )
    bot.add_handler(
        MessageHandler(
            send_user_settings,
            filters=command(BotCommands.UserSetCommand, case_sensitive=True)
            & CustomFilters.authorized_uset,
        )
    )

    # Public service commands.
    bot.add_handler(
        MessageHandler(start, filters=command(BotCommands.StartCommand, case_sensitive=True))
    )
    bot.add_handler(
        MessageHandler(login, filters=command(BotCommands.LoginCommand, case_sensitive=True))
    )

    # Callback routes.
    bot.add_handler(
        CallbackQueryHandler(
            edit_bot_settings, filters=regex("^botset") & CustomFilters.sudo
        )
    )
    bot.add_handler(CallbackQueryHandler(cancel_all_update, filters=regex("^canall")))
    bot.add_handler(CallbackQueryHandler(cancel_multi, filters=regex("^stopm")))
    bot.add_handler(CallbackQueryHandler(confirm_selection, filters=regex("^sel")))
    bot.add_handler(CallbackQueryHandler(arg_usage, filters=regex("^help")))
    bot.add_handler(
        CallbackQueryHandler(
            confirm_restart, filters=regex("^botrestart") & CustomFilters.sudo
        )
    )
    bot.add_handler(CallbackQueryHandler(pics_callback, filters=regex("^images")))
    bot.add_handler(CallbackQueryHandler(status_pages, filters=regex("^status")))
    bot.add_handler(CallbackQueryHandler(stats_pages, filters=regex("^stats")))
    bot.add_handler(CallbackQueryHandler(log_cb, filters=regex("^log")))
    bot.add_handler(CallbackQueryHandler(start_cb, filters=regex("^start")))
    bot.add_handler(CallbackQueryHandler(edit_user_settings, filters=regex("^userset")))

    if Config.SET_COMMANDS:
        await bot.set_bot_commands(
            [
                BotCommand(
                    commands[0] if isinstance(commands, list) else commands,
                    BOT_COMMANDS.get(key, "Bot command")[:256],
                )
                for key in BotCommands.get_commands()
                for commands in [getattr(BotCommands, f"{key}Command", None)]
                if commands is not None
            ]
        )
