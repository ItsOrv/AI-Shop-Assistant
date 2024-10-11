from bot import SupportBot
import asyncio

if __name__ == '__main__':
    bot = SupportBot()
    asyncio.run(bot.start())
