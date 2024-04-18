import typing
from urllib.parse import urlencode, urljoin

import aiohttp
from aiohttp import TCPConnector
from aiohttp.client import ClientSession

from app.base.base_accessor import BaseAccessor
from app.store.vk_api.dataclasses import Message, Update, UpdateObject, UpdateMessage
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
        self.session = aiohttp.ClientSession(connector=TCPConnector(verify_ssl=False))
        try:
            await self._get_long_poll_service()
        except Exception as e:
            self.logger.error("Exception", exc_info=e)

        self.poller = Poller(self.app.store)
        self.logger.info("Start polling")
        await self.poller.start()

    async def disconnect(self, app: "Application"):
        if self.session:
            await self.session.close()

        if self.poller:
            await self.poller.stop()

    @staticmethod
    def _build_query(host: str, method: str, params: dict) -> str:
        params.setdefault("v", API_VERSION)
        return f"{urljoin(host, method)}?{urlencode(params)}"

    async def _get_long_poll_service(self):
        url = 'https://api.vk.com/method/groups.getLongPollServer'
        params = {
            'group_id': self.app.config.bot.group_id,
            'access_token': self.app.config.bot.token,
            'v': API_VERSION
        }

        async with self.session.get(url, params=params) as response:
            data = await response.json()

            if 'response' in data:
                self.server = data['response']['server']
                self.key = data['response']['key']
                self.ts = data['response']['ts']
            else:
                print('Ошибка при получении сессии Long Poll сервера')

    #TODO Переписать get() как в функции выше
    async def poll(self):
        async with self.app.store.vk_api.session.get(
                f"https://lp.vk.com/whp/{self.app.store.app.config.bot.group_id}?act=a_check&key={self.key}&ts={self.ts}&wait=25") as response:
            data = await response.json()
            self.ts = data.get("ts")

            updates = [
                Update(
                    type=update["type"],
                    object=UpdateObject(
                        message=UpdateMessage(
                            id=update["object"]["message"]["id"],
                            from_id=["object"]["message"]["from_id"],
                            text=["object"]["message"]["text"],
                        )
                    )
                )
                for update in data.get("updates")
            ]

            await self.app.store.bots_manager.handle_updates(updates)

    # TODO Переписать get() как в функции выше
    async def send_message(self, message: Message) -> None:
        url = f"https://api.vk.com/method/messages.send?user_id={message.user_id}&message={message.text}&access_token={self.app.config.bot.token}"
        await self.session.post(url)
