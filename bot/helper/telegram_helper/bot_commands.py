from ...core.config_manager import Config


class BotCommands:
    StartCommand = "start"
    LoginCommand = "login"

    # Leech-only build: cloud upload, clone and search commands
    # are intentionally not registered.
    _static_commands = {
        "Leech": ["leech", "l"],
        "QbLeech": ["qbleech", "ql"],
        "JdLeech": ["jdleech", "jl"],
        "NzbLeech": ["nzbleech", "nl"],
        "Users": "users",
        "CancelTask": ["cancel", "c"],
        "CancelAll": ["cancelall", "call"],
        "ForceStart": ["forcestart", "fs"],
        "Status": ["status", "s", "statusall"],
        "MediaInfo": ["mediainfo", "mi"],
        "Ping": "ping",
        "Restart": ["restart", "r", "restartall"],
        "RestartSessions": ["restartses", "rses"],
        "Broadcast": ["broadcast", "bc"],
        "Stats": ["stats", "st"],
        "Help": ["help", "h"],
        "Log": "log",
        "Shell": "shell",
        "AExec": "aexec",
        "Exec": "exec",
        "ClearLocals": "clearlocals",
        "AddImage": ["addimage", "ai"],
        "Images": ["images", "img"],
        "Authorize": ["authorize", "a"],
        "UnAuthorize": ["unauthorize", "ua"],
        "AddSudo": ["addsudo", "as"],
        "RmSudo": ["rmsudo", "rs"],
        "BlackList": ["blacklist", "bl"],
        "RmBlackList": ["rmblacklist", "rbl"],
        "BotSet": ["bsetting", "bs"],
        "UserSet": ["usetting", "us"],
        "Select": ["select", "sel"],
        "GenPyroSess": "exportsession",
    }

    @classmethod
    def get_commands(cls):
        return cls._static_commands.copy()

    @classmethod
    def _build_command_vars(cls):
        for key, cmds in cls.get_commands().items():
            value = (
                [
                    f"{cmd}{Config.CMD_SUFFIX}"
                    if cmd not in ["restartall", "statusall"]
                    else cmd
                    for cmd in cmds
                ]
                if isinstance(cmds, list)
                else f"{cmds}{Config.CMD_SUFFIX}"
            )
            setattr(cls, f"{key}Command", value)

    @classmethod
    def refresh_commands(cls):
        cls._build_command_vars()


BotCommands._build_command_vars()
