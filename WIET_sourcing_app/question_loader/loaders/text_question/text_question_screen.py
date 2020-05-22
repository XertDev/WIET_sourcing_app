import asyncio
from asyncio import Task

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDCheckbox


class AnswerTextFieldWidget(MDTextField):
    pass


class SingleAnswerCheck(MDCheckbox):
    pass


class MultipleAnswerCheck(MDCheckbox):
    pass


class TextQuestionScreen(Screen):
    pass
