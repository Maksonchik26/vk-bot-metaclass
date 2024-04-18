from aiohttp.web_exceptions import HTTPUnprocessableEntity, HTTPConflict, HTTPNotFound, HTTPBadRequest
from aiohttp_apispec import docs, request_schema, response_schema, querystring_schema

from app.quiz.schemes import (ThemeSchema, AddThemeSchema, AddQuestionSchema, ResponseThemeSchema,
                              ResponseListThemeSchema, ResponseQuestionSchema, QuestionSchema, GetListQuestionSchema)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response, error_json_response


class ThemeAddView(View):
    @docs(tags=["quiz"], summary="Add quiz theme", description="Add quiz theme")
    @request_schema(AddThemeSchema)
    @response_schema(ResponseThemeSchema, 201)
    async def post(self):
        await AuthRequiredMixin.check_auth_admin(self.request, self.request.app)
        title = self.request["data"]["title"]
        if title in [theme.title for theme in await self.request.app.store.quizzes.list_themes()]:
            raise HTTPConflict
        theme = await self.store.quizzes.create_theme(title=title)

        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(View, AuthRequiredMixin):
    @docs(tags=["quiz"], summary="Ger list of themes", description="Ger list of themes")
    @response_schema(ResponseListThemeSchema, 200)
    async def get(self):
        await AuthRequiredMixin.check_auth_admin(self.request, self.request.app)
        themes = await self.store.quizzes.list_themes()
        raw_themes = [ThemeSchema().dump(theme) for theme in themes]

        return json_response(data={"themes": raw_themes})


class QuestionAddView(View, AuthRequiredMixin):
    @docs(tags=["quiz"], summary="Add quiz question", description="Add quiz question")
    @request_schema(AddQuestionSchema)
    @response_schema(ResponseQuestionSchema, 201)
    async def post(self):
        await AuthRequiredMixin.check_auth_admin(self.request, self.request.app)
        body = self.request["data"]
        count_correct_answers = 0
        themes = await self.request.app.store.quizzes.list_themes()
        exist_titles = [question.title for question in await self.request.app.store.quizzes.list_questions()]
        for answer in body.get("answers"):
            if answer["is_correct"]:
                count_correct_answers += 1
        if count_correct_answers != 1 or len(body.get("answers")) < 2:
            raise HTTPBadRequest
        if body["title"] in exist_titles:
            raise HTTPConflict
        theme_ids = [theme.id for theme in await self.request.app.store.quizzes.list_themes()]
        if body["theme_id"] not in theme_ids:
            raise HTTPNotFound
        question = await self.store.quizzes.create_question(body["title"], body["theme_id"], body["answers"])

        return json_response(data=QuestionSchema().dump(question))


class QuestionListView(View, AuthRequiredMixin):
    @docs(tags=["quiz"], summary="List question", description="List question")
    @querystring_schema(GetListQuestionSchema)
    @response_schema(ResponseQuestionSchema, 201)
    async def get(self):
        await AuthRequiredMixin.check_auth_admin(self.request, self.request.app)
        theme_id = await self.request.app.store.quizzes.get_theme_by_id(self.request.query.get("theme_id"))
        questions = await self.request.app.store.quizzes.list_questions(theme_id)
        raw_data = [QuestionSchema().dump(question) for question in questions]

        return json_response(data={"questions": raw_data})
