import aiohttp_session
from aiohttp.web_exceptions import HTTPUnauthorized, HTTPForbidden

from app.admin.models import Admin
from app.web.app import Request, Application
from app.web.utils import hash_password


class AuthRequiredMixin:
    @staticmethod
    async def auth_admin(request: Request, app: Application, data: dict) -> dict | None:
        if not data.get("email") or not data.get("password"):
            raise HTTPForbidden

        for admin in app.database.admins:
            if data["email"] == admin.email and hash_password(data["password"]) == admin.password:
                session = await aiohttp_session.new_session(request)
                session["email"] = admin.email
                session["password"] = admin.password

                return {"id": admin.id, "email": admin.email}

        raise HTTPForbidden

    @staticmethod
    async def check_auth_admin(request: Request, app: Application) -> Admin | None:
        session = await aiohttp_session.get_session(request)
        email = session.get("email")
        password = session.get("password")

        if not email or not password:
            raise HTTPUnauthorized

        for admin in app.database.admins:
            if email == admin.email and password == admin.password:
                return admin

        raise HTTPForbidden
