from WIET_sourcing_app.question_loader.abstract_question_loader import AbstractQuestionLoader

from .solve_mode import set_screen_view

ON_QUERY = """
TextQuestionNode{
    multiAnswer
    question
    answers
}
"""


class TextQuestionLoader(AbstractQuestionLoader):
    @staticmethod
    def get_typename() -> str:
        return "TextQuestionNode"

    @staticmethod
    def get_screen_name():
        return "TextQuestionScreen"

    @staticmethod
    def get_on_query():
        return ON_QUERY

    @staticmethod
    def set_screen_view(screen, question):
        set_screen_view(screen, question)
