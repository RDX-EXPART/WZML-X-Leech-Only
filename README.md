# WZML-X Leech-Only

A reduced build of `SilentDemonSD/WZML-X` (`wzv3`) that downloads files and uploads them only to each user's saved Telegram dump channel.

## Included

- `/leech` — direct links and Telegram files
- `/qbleech` — magnets and torrent files
- `/jdleech` — JDownloader links (when enabled)
- `/nzbleech` — NZB files/links (when enabled)
- Status, cancellation, file selection, media info and owner tools

## Removed

- Mirror/cloud-upload commands and destinations
- Google Drive/Rclone clone, delete, count and search commands
- YT-DLP and YouTube upload features
- Uphoster uploads
- RSS and torrent-search commands
- Mirror, FF Media, General, Misc and cloud sections from User Settings
- Bot PM delivery

## Required dump-channel flow

1. The user runs `/usetting`.
2. Tap **Set Dump**.
3. Add the bot as an administrator in the target channel.
4. Send the channel ID, `@username`, or `channel_id|topic_id`.
5. Leech commands remain blocked until this is completed.

The `-up` argument is rejected. A global `LEECH_DUMP_CHAT`, `BOT_PM=True`, or old database `BOT_PM` value cannot bypass the policy.

## Deploy

Copy `config_sample.py` to `config.py`, fill the required values, then run:

```bash
docker build -t wzml-leech-only .
docker run -d --name wzml-leech-only --restart unless-stopped wzml-leech-only
```

MongoDB is recommended so users' dump-channel settings remain saved after restart.
