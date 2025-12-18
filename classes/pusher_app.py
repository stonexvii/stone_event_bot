import hashlib
import hmac
import json
import time
from urllib.parse import urlencode

import aiohttp

import config
from .messages import PusherMessage


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
        self._message: PusherMessage | None = None

    def set_message(self, message: PusherMessage):
        self._message = message

    def set_title(self, title: str):
        self._message.set_title(title)

    async def set_question(self, question: str):
        self._message.set_question(question)
        await self.push()

    async def set_answer(self, answer_id: int, **kwargs):
        self._message.set_answer(answer_id, **kwargs)
        await self.push()

    async def reset(self):
        self._message.reset()
        await self.push()

    async def set_top5(self, **kwargs):
        self._message.set_question(kwargs['question'])
        for answer_idx, answer in kwargs.items():
            if answer_idx != 'question':
                self._message.set_answer(answer_idx, **answer)
        await self.push()

    async def push(self, name: str = 'my-event', channel: str = 'my-channel'):
        pass
        # print(self._message.json)
        method, path = "POST", f"/apps/{self.app_id}/events"
        body = json.dumps(
            {
                "name": name,
                "channels": [channel],
                "data": self._message.json,
            },
        )
        print(self._message.json)
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
