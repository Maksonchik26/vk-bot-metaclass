from aiohttp.web_exceptions import HTTPUnprocessableEntity, HTTPConflict, HTTPNotFound
from aiohttp_apispec import docs, request_schema, response_schema, querystring_schema

from app.quiz.schemes import (ThemeSchema, AddThemeSchema, AddQuestionSchema, ResponseThemeSchema,
                              ResponseListThemeSchema, ResponseQuestionSchema, QuestionSchema, GetListQuestionSchema)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class ThemeAddView(View, AuthRequiredMixin):
    @docs(tags=["quiz"], summary="Add quiz theme", description="Add quiz theme")
    @request_schema(AddThemeSchema)
    @response_schema(ResponseThemeSchema, 201)
    async def post(self):
        await self.check_auth()
        title = self.request["data"]["title"]
        if title in [theme.title for theme in await self.request.app.store.quizzes.list_themes()]:
            raise HTTPUnprocessableEntity
        theme = await self.store.quizzes.create_theme(title=title)
        print(self.request.app.database.questions, self.request.app.database.themes)
        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(View, AuthRequiredMixin):
    @docs(tags=["quiz"], summary="Ger list of themes", description="Ger list of themes")
    @response_schema(ResponseListThemeSchema, 200)
    async def get(self):
        await self.check_auth()
        themes = await self.store.quizzes.list_themes()
        raw_themes = [ThemeSchema().dump(theme) for theme in themes]

        return json_response(data={"themes": raw_themes})


class QuestionAddView(View, AuthRequiredMixin):
    @docs(tags=["quiz"], summary="Add quiz question", description="Add quiz question")
    @request_schema(AddQuestionSchema)
    @response_schema(ResponseQuestionSchema, 201)
    async def post(self):
        await self.check_auth()
        body = self.request["data"]
        count_correct_answers = 0
        exist_titles = [question.title for question in await self.request.app.store.quizzes.list_questions()]
        for answer in body.get("answers"):
            if answer["is_correct"]:
                count_correct_answers += 1
        if count_correct_answers != 1 or len(body.get("answers")) < 2:
            raise HTTPUnprocessableEntity
        if body["title"] in exist_titles:
            raise HTTPConflict
        if body["theme_id"] not in [theme.id for theme in await self.request.app.store.quizzes.list_themes()]:
            raise HTTPNotFound
        question = await self.store.quizzes.create_question(body["title"], body["theme_id"], body["answers"])

        return json_response(data=QuestionSchema().dump(question))


class QuestionListView(View, AuthRequiredMixin):
    @docs(tags=["quiz"], summary="List question", description="List question")
    @querystring_schema(GetListQuestionSchema)
    @response_schema(ResponseQuestionSchema, 201)
    async def get(self):
        await self.check_auth()
        theme_id = await self.request.app.store.quizzes.get_theme_by_id(self.request.query["theme_id"])
        questions = await self.request.app.store.quizzes.list_questions(theme_id)
        raw_data = [QuestionSchema().dump(question) for question in questions]

        return json_response(data={"questions": raw_data})
