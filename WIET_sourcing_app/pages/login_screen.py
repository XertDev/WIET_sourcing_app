from random import random

from kivy.app import App
from kivy.uix.screenmanager import Screen

import threading

from kivymd.uix.snackbar import Snackbar

green = [0, 1, 0, 1]


class LoginScreen(Screen):

	def move_to_signup(self):
		app = App.get_running_app()
		app.change_screen("signup_screen")

	def sign_in(self):
		threading.Thread(target=self.sign_in_worker).start()

	def sign_in_worker(self):
		app = App.get_running_app()
		email = self.ids.email.text
		password = self.ids.password.text
		if not app.auth_service.sign_in(email, password):
			Snackbar(text="Failed to sign in!").show()
			self.ids['button_one'].md_bg_color = app.theme_cls.error_color
			self.ids['button_one'].text_color = app.theme_cls.accent_color
		else:
			app.change_screen("main_screen")
			app.enable_drawer()