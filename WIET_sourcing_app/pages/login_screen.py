from kivy.app import App
from kivy.uix.screenmanager import Screen


class LoginScreen(Screen):
	def move_to_signup(self):
		app = App.get_running_app()
		app.change_screen("signup_screen")



