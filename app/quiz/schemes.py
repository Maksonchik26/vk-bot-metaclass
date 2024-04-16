from marshmallow import Schema, fields

from app.web.schemes import OkResponseSchema

### Theme ###
class AddThemeSchema(Schema):
    title = fields.Str(required=True)


class ThemeSchema(AddThemeSchema):
    id = fields.Int(required=True)


class ResponseThemeSchema(OkResponseSchema):
    data = fields.Nested(ThemeSchema, many=False)


class ListThemeSchema(Schema):
    themes = fields.Nested(ThemeSchema, many=True)


class ResponseListThemeSchema(OkResponseSchema):
    data = fields.Nested(ListThemeSchema)


### Answer ###
class AnswerSchema(Schema):
    title = fields.Str(required=True)
    is_correct = fields.Bool(required=True)


### Question ###
class AddQuestionSchema(Schema):
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.Nested(AnswerSchema, many=True)


class QuestionSchema(AddQuestionSchema):
    id = fields.Int(required=True)


class ResponseQuestionSchema(OkResponseSchema):
    data = fields.Nested(QuestionSchema)


class GetListQuestionSchema(Schema):
    theme_id = fields.Int(required=False)


class ResponseListQuestionSchema(OkResponseSchema):
    data = fields.Nested(QuestionSchema)
