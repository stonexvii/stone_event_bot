# import pusher
#
# import config
#
# pusher_client = pusher.Pusher(
#     app_id=config.PUSHER_APP_ID,
#     key=config.PUSHER_KEY,
#     secret=config.PUSHER_SECRET,
#     cluster=config.PUSHER_CLUSTER,
#     ssl=True,
#     timeout=15,
# )
#
#
# def push_message(message: dict[str, str]):
#     pusher_client.trigger('my-channel', 'my-event', message)


import hmac
import hashlib
import time
import json
from urllib.parse import urlencode

import aiohttp
import config


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
        self.message = {
            'question': 'HEADER',
            'answer_1': '',
            'answer_2': '',
            'answer_3': '',
            'answer_4': '',
        }

    async def trigger(self):
        method = "POST"
        path = f"/apps/{self.app_id}/events"

        body = json.dumps({
            "name": 'my-event',
            "channels": ['my-channel'],
            "data": json.dumps(self.message, ensure_ascii=False)
        })

        body_md5 = hashlib.md5(body.encode("utf-8")).hexdigest()

        params = {
            "auth_key": self.key,
            "auth_timestamp": int(time.time()),
            "auth_version": "1.0",
            "body_md5": body_md5,
        }

        sorted_params = sorted(params.items(), key=lambda x: x[0])
        query_string = urlencode(sorted_params)

        string_to_sign = f"{method}\n{path}\n{query_string}"
        signature = hmac.new(
            self.secret,
            string_to_sign.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        params["auth_signature"] = signature

        url = f"{self.base}{path}"

        headers = {
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params, data=body, headers=headers) as resp:
                text = await resp.text()
                return resp.status, text
