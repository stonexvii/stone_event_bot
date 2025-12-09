import asyncio
import aiohttp
from pathlib import Path
import os


class QRCodeApp:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, filename: str):
        self.filename = filename
        self.size = 300
        self.bg_color = "#ffffff"
        self.fg_color = "#000000"
        self.logo_url = None
        self.url = 'https://api.qrcode-monkey.com/qr/custom'
        self.base_url = 'https://t.me/stone_event_bot?start={event_id}'

    @property
    def _config(self):
        config = {
            "body": "square",
            "eye": "frame0",
            "eyeBall": "ball0",
            "bodyColor": self.fg_color,
            "bgColor": self.bg_color,
            "logo": self.logo_url or "",
            "logoMode": "default",
        }
        return config

    async def get_qr(self, event_id: int):
        payload = {
            "data": self.base_url.format(event_id=event_id),
            "config": self._config,
            "size": self.size,
            "download": False,
            "file": "png",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=payload) as resp:
                if resp.status != 200:
                    error_text = await resp.text()
                    raise RuntimeError(
                        f"Ошибка запроса: {resp.status}\nТело ответа: {error_text}"
                    )
                img_bytes = await resp.read()
        # img_bytes = await resp.read()

        return img_bytes
        # Path(os.path.join('data', self.filename)).write_bytes(img_bytes)
