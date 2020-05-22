import asyncio
from asyncio import Task

from kivy.app import App


class SolveSetMode:
    _task: Task

    def __init__(self):
        self.questions = None
        self.current_question = -1

    def load_questions(self, questions: list):
        self.questions = questions
        self.current_question = -1

    async def async_get_question_union(self, que_id, typename):
        app = App.get_running_app()
        on_query = app.question_loader_manager.get_on_query_by_typename(typename)
        res = await app.question_service.get_question_union(que_id, on_query)

        screen_name = app.question_loader_manager.get_screen_by_typename("TextQuestionNode")
        screen = app.root.ids.screen_manager.get_screen(screen_name)

        app.question_loader_manager.set_screen(screen, res)
        if self.current_question >= len(self.questions) - 1:
            screen.ids.next_question_button.text = "Prześlij swoje odpowiedzi"

        app.change_screen(screen_name, "forward")

    def show_next_question(self):
        app = App.get_running_app()
        self.current_question += 1

        if self.current_question >= len(self.questions):
            app.change_screen("main_screen", "forward")
            return

        que_id, typename = self.questions[self.current_question]
        self._task = asyncio.create_task(self.async_get_question_union(que_id, typename))