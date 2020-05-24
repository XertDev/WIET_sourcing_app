import asyncio
import threading

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.behaviors import MagicBehavior
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.snackbar import Snackbar


class MagicButton(MagicBehavior, MDRectangleFlatButton):
	pass


class SignupScreen(Screen):
	def move_to_login(self):
		app = App.get_running_app()
		app.change_screen("login_screen", "backward")

	def sign_up(self):
		app = App.get_running_app()
		asyncio.ensure_future(self.sign_up_async())

	async def sign_up_async(self):
		app = App.get_running_app()
		name = self.ids.name.text
		email = self.ids.email.text
		password = self.ids.password.text

		app.auth_service.set_email(email)

		if not await app.auth_service.sign_up(name, email, password):
			Snackbar(text="Failed to sign up!").show()
		else:
			app.change_screen("confirm_email_screen", "forward")

