import typing

from app.store.vk_api.dataclasses import Update, Message

if typing.TYPE_CHECKING:
    from app.web.app import Application


class BotManager:
    def __init__(self, app: "Application"):
        self.app = app

    async def handle_updates(self, updates: list[Update]):
        messages = [update.object.message for update in updates]
        for message in messages:
            msg = Message(message.from_id, "Hey")
            await self.app.store.vk_api.send_message(msg)

