from telethon import TelegramClient, events
from config import API_ID, API_HASH, PHONE_NUMBER, SESSION_NAME
from rag_model import RAGModel
import asyncio

class SupportBot:
    def __init__(self):
        self.client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
        self.rag_model = RAGModel()

    async def start(self):
        await self.client.start(phone=PHONE_NUMBER)
        print("Bot started!")

        @self.client.on(events.NewMessage(pattern='/start'))
        async def start_handler(event):
            await event.reply('سلام! به ربات پشتیبانی ما خوش آمدید. چطور می‌توانم به شما کمک کنم؟')

        @self.client.on(events.NewMessage)
        async def message_handler(event):
            if event.is_private:  # فقط به پیام‌های خصوصی پاسخ می‌دهد
                user_message = event.message.text
                response = await self.rag_model.generate_response(user_message)
                await event.reply(response)

        await self.client.run_until_disconnected()

if __name__ == '__main__':
    bot = SupportBot()
    asyncio.run(bot.start())
