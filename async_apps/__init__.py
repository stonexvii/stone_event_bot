from .pusher_app import AsyncPusher
from .qr_api_app import QRCodeApp

async_pusher = AsyncPusher()
qr_code_app = QRCodeApp('stone_qr.png')
