import asyncio
from asyncio import Task

from app.store import Store


class Poller:
    def __init__(self, store: Store) -> None:
        self.store = store
        self.is_running = False
        self.poll_task: Task | None = None

    async def start(self) -> None:
        self.is_running = True
        self.poll_task = asyncio.create_task(self.poll())

    async def stop(self) -> None:
        self.is_running = False
        self.poll_task.cancel()

    async def poll(self) -> None:
        ts = self.store.vk_api.ts
        while True:
            async with self.store.vk_api.session.get(f"https://lp.vk.com/whp/{self.store.app.config.bot.group_id}?act=a_check&key={self.store.vk_api.key}&ts={ts}&wait=25") as response:
                data = await response.json()
                ts = data["ts"]
                updates = data["update"]
                self.store.bots_manager.handle_updates(updates)
