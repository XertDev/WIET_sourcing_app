import concurrent.futures

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.snackbar import Snackbar

import asyncio


class ConfirmEmailScreen(Screen):

	def confirm_email(self):
		asyncio.ensure_future(self.confirm_email_async())

	async def confirm_email_async(self):
		app = App.get_running_app()
		code = self.ids.code.text
		email = app.auth_service.get_email()

		if not await app.auth_service.confirm_email(code, email):
			Snackbar(text="Failed to confirm your email!").show()
			self.ids['button_one'].md_bg_color = app.theme_cls.error_color
			self.ids['button_one'].text_color = app.theme_cls.accent_color
		else:
			app.change_screen("main_screen")
