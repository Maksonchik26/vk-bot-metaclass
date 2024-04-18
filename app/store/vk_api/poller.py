import asyncio
from asyncio import Task

from app.store import Store
from app.store.vk_api.dataclasses import Update, UpdateObject, UpdateMessage


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
        while self.is_running:
            self.store.vk_api.poll()

