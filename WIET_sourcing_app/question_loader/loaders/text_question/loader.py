from WIET_sourcing_app.question_loader.abstract_question_loader import AbstractQuestionLoader

from .text_question_screen import TextQuestionScreen

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
    def load_question(payload):
        pass