import random
import typing
import uuid

from app.admin.models import Admin
from app.base.base_accessor import BaseAccessor
from app.web.utils import hash_password

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):

    async def connect(self, app: "Application") -> None:
        self.app = app
        await self.create_admin(app.config.admin.email, app.config.admin.password)

    async def get_by_email(self, email: str) -> Admin | None:
        for admin in self.app.database.admins:
            if admin.email == email:
                return admin

        return None

    async def create_admin(self, email: str, password: str):
        admin = Admin(id=self.app.database.next_admin_id, email=email, password=hash_password(password))
        self.app.database.admins.append(admin)
