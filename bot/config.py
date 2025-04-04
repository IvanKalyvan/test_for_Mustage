import os

from dotenv import load_dotenv

load_dotenv()

webhook_secret = os.getenv("WEBHOOK_SECRET")
webhook_path = os.getenv("WEBHOOK_PATH")
webhook_base_url = os.getenv("WEBHOOK_BASE_URL")
webhook_server_host = os.getenv("WEBHOOK_SERVER_HOST")
webhook_server_port = int(os.getenv("WEBHOOK_SERVER_PORT"))
bot_key = os.getenv("BOT_KEY")
api_url = os.getenv("API_URL")

webhook_url = f"{webhook_base_url}{webhook_path}"