import logging
import sys
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.fsm.storage.memory import MemoryStorage

from routers.start import router
from routers.create import router as create_router
from routers.get import router as get_router
from routers.delete import router as delete_router
from routers.update import router as update_router
from config import bot_key, webhook_server_host, webhook_server_port, webhook_path, webhook_secret, webhook_url

storage = MemoryStorage()
bot = Bot(token=bot_key, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)
dp.include_router(router)
dp.include_router(create_router)
dp.include_router(get_router)
dp.include_router(delete_router)
dp.include_router(update_router)

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger()

async def on_startup(bot: Bot) -> None:

    await bot.set_webhook(f"{webhook_url}", secret_token=webhook_secret)


def main() -> None:

    router.message.middleware()(lambda handler, event,
                                data: handler(event, {**data, 'bot': bot}))
    dp.startup.register(on_startup)
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp, bot=bot, secret_token=webhook_secret)
    webhook_requests_handler.register(app, path=webhook_path)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=webhook_server_host, port=webhook_server_port)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()