import asyncio
from asyncio import Task
from time import sleep
from functools import partial

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton

from WIET_sourcing_app.loaders.question_set_loader import QuestionLoaderManager


class SetButton(MDRectangleFlatButton):
	def __init__(self, set_id, **kwargs):
		self.set_id = set_id
		super().__init__(**kwargs)


class MainScreen(Screen):
	_task: Task

	def on_pre_enter(self, *args):
		self._task = asyncio.create_task(self.query_user_info())
		self._task = asyncio.create_task(self.query_question_sets())
		super().on_pre_enter(*args)

	def on_pre_leave(self, *args):
		self._task.cancel()

	def update_view(self):
		app = App.get_running_app()
		self.ids.username.text = app.user_service.user_info.name

	async def query_user_info(self):
		while True:
			app = App.get_running_app()

			await app.user_service.update_reload_user_info()
			self.update_view()
			await asyncio.sleep(10)

	async def query_question_sets(self):
		app = App.get_running_app()
		question_sets = await app.question_set_service.query_question_sets()
		for question_set in question_sets:
			self.ids.set_list.add_widget(
				SetButton(text=question_set.name+" "+str(question_set.question_count),
						set_id=question_set.id,
						on_press=partial(QuestionLoaderManager.load_set_questions, ''))
			)
