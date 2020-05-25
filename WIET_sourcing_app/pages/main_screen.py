import asyncio
from asyncio import Task
from time import sleep

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel

from WIET_sourcing_app.data_providers.question_set_list_provider import QuestionSetListProvider

from WIET_sourcing_app.widgets.data_table import data_table
from WIET_sourcing_app.widgets.data_table.data_table import DataTable


class MainScreen(Screen):
	_task: Task
	_table: DataTable

	def on_pre_enter(self, *args):
		self._task = asyncio.create_task(self.query_user_info())
		#self._task = asyncio.create_task(self.query_question_sets())
		self._table = DataTable(QuestionSetListProvider())
		self.ids.central.add_widget(self._table)
		super().on_pre_enter(*args)


	def on_pre_leave(self, *args):
		self.ids.central.remove_widget(self._table)
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
				MDLabel(text=question_set.name+" "+str(question_set.question_count))
			)
