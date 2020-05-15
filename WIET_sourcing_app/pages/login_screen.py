import concurrent.futures

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.snackbar import Snackbar

import asyncio


class LoginScreen(Screen):

	def move_to_signup(self):
		app = App.get_running_app()
		app.change_screen("signup_screen")

	def sign_in(self):
		asyncio.ensure_future(self.sign_in_async())

	async def sign_in_async(self):
		app = App.get_running_app()
		email = self.ids.email.text
		password = self.ids.password.text

		if not await app.auth_service.sign_in(email, password):
			Snackbar(text="Failed to sign in!").show()
		else:
			app.change_screen("main_screen")
			app.enable_drawer()
