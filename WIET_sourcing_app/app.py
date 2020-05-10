import sys

import kivy
from kivy import Config
import kivy.utils
from kivy.core.window import Window
from kivy.uix.screenmanager import SlideTransition, NoTransition, CardTransition
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel

from WIET_sourcing_app.pages.login_screen import LoginScreen
from WIET_sourcing_app.pages.signup_screen import SignupScreen

sys.path.append("/".join(x for x in __file__.split("/")[:-1]))

kivy.require('1.0.7')

Config.set('graphics', 'fullscreen', '0')

Window.minimum_height = 500
Window.minimum_width = 600


class WIETSourcingApp(MDApp):
	def change_screen(self, screen_name, direction='forward'):
		screen_manager = self.root.ids['screen_manager']
		if direction == 'forward':
			direction = 'left'
		elif direction == 'backward':
			direction = 'right'
		elif direction == "None":
			screen_manager.transition = NoTransition()
			screen_manager.current = screen_name
			return

		screen_manager.transition = SlideTransition(direction=direction)

		screen_manager.current = screen_name

	def hello(self):
		print("hello")
