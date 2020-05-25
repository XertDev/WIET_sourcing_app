from .text_question_screen import TextQuestionScreen, SingleAnswerCheck, MultipleAnswerCheck, AnswerTextFieldWidget
from kivymd.uix.label import MDLabel


def set_screen_view(screen, question):
    screen.ids.user_input_layout.clear_widgets()
    screen.ids.label_test.text = question["question"]

    for k in range(len(question["answers"])):
        que = question["answers"][k]
        screen.ids.user_input_layout.add_widget(MultipleAnswerCheck(stored_index=k) if question["multiAnswer"]
                                                else SingleAnswerCheck(stored_index=k))
        screen.ids.user_input_layout.add_widget(MDLabel(text=que))

    if len(question["answers"]) == 0:
        screen.ids.user_input_layout.add_widget(AnswerTextFieldWidget())
