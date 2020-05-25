from WIET_sourcing_app.question_loader.abstract_question_loader import AbstractQuestionLoader

from .solve_mode import set_screen_view
from .text_question_screen import SingleAnswerCheck, MultipleAnswerCheck

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
    def get_create_answer_mutation(screen, question_id):
        widgets = screen.ids.user_input_layout.children
        indices = []
        for widget in widgets:
            if isinstance(widget, SingleAnswerCheck) or isinstance(widget, MultipleAnswerCheck):
                if widget.active:
                    indices.append(widget.stored_index)
        return "createTextQuestionAnswer(questionNodeId: \"%s\", answerIndices: %s)" \
               % (str(question_id), str(indices))

    @staticmethod
    def set_screen_view(screen, question):
        set_screen_view(screen, question)
