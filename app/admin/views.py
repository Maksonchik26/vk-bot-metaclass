import aiohttp_session
from aiohttp.web_exceptions import HTTPUnauthorized, HTTPForbidden

from app.web.app import View
from aiohttp_apispec import docs, request_schema, response_schema

from app.admin.schemes import LoginAdminRequestSchema, AdminResponseSchema, AdminSchema
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class AdminLoginView(View, AuthRequiredMixin):
    @docs(tags=["admin"], summary="Login admin", description="Login admin in the app")
    @request_schema(LoginAdminRequestSchema)
    @response_schema(AdminResponseSchema, 201)
    async def post(self):
        data = self.request["data"]
        await self.check_credentials(data)

        session = await aiohttp_session.new_session(self.request)
        session["email"] = data["email"]
        session["password"] = data["password"]
        loginned_admin = await self.request.app.store.admins.get_by_email(session["email"])
        data = AdminSchema().dump(loginned_admin)

        return json_response(data=data)


class AdminCurrentView(View, AuthRequiredMixin):
    @docs(tags=["admin"], summary="Get current admin", description="Get current admin")
    @response_schema(AdminResponseSchema, 201)
    async def get(self):
        session = await aiohttp_session.get_session(self.request)
        await self.check_auth()
        current_admin = await self.request.app.store.admins.get_by_email(session.get("email"))
        data = AdminSchema().dump(current_admin)

        return json_response(data=data)
