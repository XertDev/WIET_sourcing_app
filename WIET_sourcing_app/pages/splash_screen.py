import asyncio

from kivy.app import App
from kivy.uix.screenmanager import Screen


class SplashScreen(Screen):
	def on_enter(self, *args):
		asyncio.ensure_future(self.load_auth_state())
		super().on_enter(*args)

	async def load_auth_state(self):
		app = App.get_running_app()
		await asyncio.sleep(1)
		if await app.auth_service.load_auth_token_from_store():
			app.change_screen("main_screen", "forward")
		else:
			app.change_screen("login_screen", "forward")

