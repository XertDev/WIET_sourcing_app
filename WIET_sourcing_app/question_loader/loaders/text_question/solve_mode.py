from .text_question_screen import TextQuestionScreen, SingleAnswerCheck, MultipleAnswerCheck, AnswerTextFieldWidget
from kivymd.uix.label import MDLabel


def set_screen_view(screen, question):
    screen.ids.user_input_layout.clear_widgets()
    screen.ids.label_test.text = question["question"]

    for que in question["answers"]:
        screen.ids.user_input_layout.add_widget(MultipleAnswerCheck() if question["multiAnswer"]
                                                else SingleAnswerCheck())
        screen.ids.user_input_layout.add_widget(MDLabel(text=que))

    if len(question["answers"]) == 0:
        screen.ids.user_input_layout.add_widget(AnswerTextFieldWidget())
