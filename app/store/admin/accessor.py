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
        password = hash_password(f"{app.config.admin.email}:{app.config.admin.password}")
        admin = await self.create_admin(app.config.admin.email, password)
        app.database.admins.append(admin)

    async def get_by_email(self, email: str) -> Admin | None:
        for admin in self.app.database.admins:
            if admin.email == email:
                return admin
        return None

    async def create_admin(self, email: str, password: str) -> Admin:
        admin = Admin(id=1, email=email, password=password) #TODO Поправить id=
        return admin
