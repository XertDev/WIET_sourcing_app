from kivy.app import App
from kivy.uix.screenmanager import Screen


class SignupScreen(Screen):
	def move_to_login(self):
		app = App.get_running_app()
		app.change_screen("login_screen", "backward")
