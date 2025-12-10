import hashlib
import hmac
import json
import time
from urllib.parse import urlencode

import aiohttp

import config
from .opinions_message import PusherMessage


class AsyncPusher:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, ssl=True):
        self.app_id = config.PUSHER_APP_ID
        self.key = config.PUSHER_KEY
        self.secret = config.PUSHER_SECRET.encode()
        self.cluster = config.PUSHER_CLUSTER
        self.scheme = "https" if ssl else "http"
        self.base = f"{self.scheme}://api-{self.cluster}.pusher.com"
        self.message = PusherMessage()

    async def set_question(self, question: str):
        self.message.set_question(question)
        await self.push()

    async def set_answer(self, answer_id: int, answer: str):
        self.message.set_answer(answer_id, answer)
        await self.push()

    async def reset(self):
        self.message.reset()
        await self.push()

    async def push(self, name: str = 'my-event', channel: str = 'my-channel'):
        method, path = "POST", f"/apps/{self.app_id}/events"
        body = json.dumps({
            "name": name,
            "channels": [channel],
            "data": json.dumps(self.message.json, ensure_ascii=False)
        })

        params = {
            "auth_key": self.key,
            "auth_timestamp": int(time.time()),
            "auth_version": "1.0",
            "body_md5": hashlib.md5(body.encode("utf-8")).hexdigest(),
        }

        sorted_params = sorted(params.items(), key=lambda x: x[0])
        string_to_sign = f"{method}\n{path}\n{urlencode(sorted_params)}"
        signature = hmac.new(
            self.secret,
            string_to_sign.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        params["auth_signature"] = signature
        headers = {
            "Content-Type": "application/json"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base}{path}", params=params, data=body, headers=headers) as resp:
                text = await resp.text()
                return resp.status, text
