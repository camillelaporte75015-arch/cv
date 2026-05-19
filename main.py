from telethon import TelegramClient
from telethon.errors import FloodWaitError
import asyncio

api_id = 34851852
api_hash = "44d65a2b2fd2febf46c9062b48878f6b"

SOURCE_CHAT = "incultescrow"
MESSAGE_ID = 13

client = TelegramClient("session", api_id, api_hash)


async def get_channels():
    channels = []

    async for dialog in client.iter_dialogs():
        entity = dialog.entity

        if getattr(entity, "broadcast", False) or getattr(entity, "megagroup", False):
            channels.append(entity)

    return channels


async def main():
    await client.start()
    print("Userbot connecté")

    source = await client.get_entity(SOURCE_CHAT)

    while True:
        try:
            msg = await client.get_messages(source, ids=MESSAGE_ID)

            if not msg:
                print("Message introuvable")
                await asyncio.sleep(60)
                continue

            channels = await get_channels()
            print(f"{len(channels)} canaux trouvés")

            for channel in channels:
                try:
                    await client.forward_messages(channel, msg)
                    print(f"Envoyé -> {getattr(channel, 'title', 'Sans nom')}")
                    await asyncio.sleep(3)

                except FloodWaitError as e:
                    print(f"FloodWait {e.seconds}s")
                    await asyncio.sleep(e.seconds)

                except Exception as e:
                    print(f"Erreur {getattr(channel, 'title', 'unknown')} : {e}")

            print("Cycle terminé → cooldown 60 secondes")
            await asyncio.sleep(60)

        except Exception as e:
            print(f"Erreur globale: {e}")
            await asyncio.sleep(60)


with client:
    client.loop.run_until_complete(main())
