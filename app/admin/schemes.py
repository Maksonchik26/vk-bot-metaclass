from marshmallow import Schema, fields

from app.web.schemes import OkResponseSchema


class DefaultAdminSchema(Schema):
    email = fields.Str(required=True)


class LoginAdminRequestSchema(DefaultAdminSchema):
    password = fields.Str(required=True)


class AdminSchema(DefaultAdminSchema):
    id = fields.Integer(required=True)


class AdminResponseSchema(OkResponseSchema):
    data = fields.Nested(AdminSchema)
