import asyncio
from asyncio import Task
from time import sleep

from kivy.app import App
from kivy.uix.screenmanager import Screen


class MainScreen(Screen):
	_task: Task

	def on_pre_enter(self, *args):
		self._task = asyncio.create_task(self.update_user_info())
		super().on_pre_enter(*args)

	def on_pre_leave(self, *args):
		self._task.cancel()

	def update_view(self):
		app = App.get_running_app()
		self.ids.username.text = app.user_service.user_info.name

	async def update_user_info(self):
		app = App.get_running_app()

		await app.user_service.update_reload_user_info()
		self.update_view()
		await asyncio.sleep(10)


