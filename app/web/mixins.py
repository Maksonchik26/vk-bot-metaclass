import aiohttp_session
from aiohttp.web_exceptions import HTTPUnauthorized, HTTPForbidden


class AuthRequiredMixin:


    def __init__(self):
        self.request = None

    async def check_credentials(self, data):
        if not (data["email"] == self.request.app.config.admin.email and data["password"]
                == self.request.app.config.admin.password):
            raise HTTPForbidden
        
        return

    async def check_auth(self):
        session = await aiohttp_session.get_session(self.request)
        if not session.get("email") or not session.get("password"):
            raise HTTPUnauthorized
        if not await self.request.app.store.admins.get_by_email(session.get("email")):
            raise HTTPForbidden

        return
