import asyncio
from telethon import TelegramClient, events

api_id = 28990846
api_hash = "28962aebadaffac1b652586caa07fad9"

SOURCE_USER_ID = 1602683344
TARGET_CHANNEL_ID = -1003738237609

client = TelegramClient("session", api_id, api_hash)


@client.on(events.NewMessage())
async def handler(event):
    try:
        sender = await event.get_sender()

        # 🔍 проверяем отправителя
        if not sender:
            return

        if sender.id != SOURCE_USER_ID:
            return

        text = event.raw_text or ""

        print(f"📩 Пришло сообщение: {text}")

        # 🔍 проверяем текст
        if "У тебя новое анонимное сообщение!" in text:
            print("✅ Нашёл нужное сообщение")

            # ❗ пробуем форвард
            try:
                await event.forward_to(TARGET_CHANNEL_ID)
                print("📤 Переслал нормально")
            except Exception as e:
                print("🚫 Форвард не работает, копирую")

                await client.send_message(
                    TARGET_CHANNEL_ID,
                    event.message,
                    formatting_entities=event.message.entities
                )

    except Exception as e:
        print(f"❌ Ошибка: {e}")


async def main():
    print("🚀 Бот запущен...")
    await client.run_until_disconnected()


with client:
    client.loop.run_until_complete(main())