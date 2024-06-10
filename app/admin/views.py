from app.web.app import View
from aiohttp_apispec import docs, request_schema, response_schema

from app.admin.schemes import LoginAdminRequestSchema, AdminResponseSchema, AdminSchema
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class AdminLoginView(View):
    @docs(tags=["admin"], summary="Login admin", description="Login admin in the app")
    @request_schema(LoginAdminRequestSchema)
    @response_schema(AdminResponseSchema, 200)
    async def post(self):
        data = self.request["data"]
        data_json = await AuthRequiredMixin.auth_admin(self.request, self.request.app, data)

        return json_response(data=data_json)


class AdminCurrentView(View):
    @docs(tags=["admin"], summary="Get current admin", description="Get current admin")
    @response_schema(AdminResponseSchema, 200)
    async def get(self):
        admin = await AuthRequiredMixin.check_auth_admin(self.request, self.request.app)

        return json_response(AdminSchema().dump(admin))
