import os

import dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
# CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
OPENAI_API_KEY = os.getenv('OPENAI_TOKEN')
PROXY = os.getenv('PROXY')

DB_NAME = os.getenv('DB_NAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_USER = os.getenv('DB_USER')
DB_ADDRESS = os.getenv('DB_ADDRESS')
DB_PORT = int(os.getenv('DB_PORT'))

DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}:{DB_PORT}/{DB_NAME}'

PUSHER_APP_ID = os.getenv('PUSHER_APP_ID')
PUSHER_KEY = os.getenv('PUSHER_KEY')
PUSHER_SECRET = os.getenv('PUSHER_SECRET')
PUSHER_CLUSTER = os.getenv('PUSHER_CLUSTER')