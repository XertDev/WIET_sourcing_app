import asyncio
from asyncio import Task

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDCheckbox


class AnswerTextFieldWidget(MDTextField):
    pass


class SingleAnswerCheck(MDCheckbox):
    def __init__(self, stored_index, **kwargs):
        self.stored_index = stored_index
        super().__init__(**kwargs)


class MultipleAnswerCheck(MDCheckbox):
    def __init__(self, stored_index, **kwargs):
        self.stored_index = stored_index
        super().__init__(**kwargs)


class TextQuestionScreen(Screen):
    pass
