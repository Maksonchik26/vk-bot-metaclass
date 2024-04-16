import typing
from urllib.parse import urlencode, urljoin

import aiohttp
from aiohttp.client import ClientSession

from app.base.base_accessor import BaseAccessor
from app.store.vk_api.dataclasses import Message
from app.store.vk_api.poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application

API_VERSION = "5.131"


class VkApiAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: ClientSession | None = None
        self.key: str | None = None
        self.server: str | None = None
        self.poller: Poller | None = None
        self.ts: int | None = None

    async def connect(self, app: "Application"):

        url = 'https://api.vk.com/method/groups.getLongPollServer'
        params = {
            'group_id': self.app.config.bot.group_id,
            'access_token': self.app.config.bot.token,
            'v': API_VERSION
        }

        self.session = aiohttp.ClientSession()
        async with self.session.get(url, params=params) as response:
            data = await response.json()

            if 'response' in data:
                self.server = data['response']['server']
                self.key = data['response']['key']
                self.ts = data['response']['ts']
            else:
                print('Ошибка при получении сессии Long Poll сервера')

            self.poller = Poller(self.app.store)
            await self.poller.start()

    async def disconnect(self, app: "Application"):
        self.session.close()

    @staticmethod
    def _build_query(host: str, method: str, params: dict) -> str:
        params.setdefault("v", API_VERSION)
        return f"{urljoin(host, method)}?{urlencode(params)}"

    async def _get_long_poll_service(self):
        pass

    async def poll(self):
        pass

    async def send_message(self, message: Message) -> None:
        url = f"https://api.vk.com/method/messages.send?user_id={message.user_id}&message={message.text}"
        await self.session.post(url)
