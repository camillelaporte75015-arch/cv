from telethon import TelegramClient
from telethon.errors import FloodWaitError
import asyncio

api_id = 12345678
api_hash = "TON_API_HASH"

SOURCE_CHAT = "incultescrow"   # ou ID / username
MESSAGE_ID = 13

client = TelegramClient("session", api_id, api_hash)


async def get_channels():
    channels = []

    async for dialog in client.iter_dialogs():
        entity = dialog.entity

        # groupes + channels uniquement
        if getattr(entity, "broadcast", False) or getattr(entity, "megagroup", False):
            channels.append(entity)

    return channels


async def main():
    await client.start()
    print("Userbot connecté")

    # récupère le message source
    source = await client.get_entity(SOURCE_CHAT)
    msg = await client.get_messages(source, ids=MESSAGE_ID)

    if not msg:
        print("Message introuvable")
        return

    channels = await get_channels()
    print(f"{len(channels)} canaux trouvés")

    for channel in channels:
        try:
            await client.forward_messages(channel, msg)
            print(f"Envoyé -> {getattr(channel, 'title', 'Sans nom')}")

            await asyncio.sleep(2)

        except FloodWaitError as e:
            print(f"Flood wait {e.seconds}s")
            await asyncio.sleep(e.seconds)

        except Exception as e:
            print(f"Erreur: {e}")

    print("Terminé.")


with client:
    client.loop.run_until_complete(main())
