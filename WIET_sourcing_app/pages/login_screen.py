from kivy.app import App
from kivy.uix.screenmanager import Screen


class LoginScreen(Screen):
	def move_to_signup(self):
		app = App.get_running_app()
		app.change_screen("signup_screen")

	def sign_in(self):
		app = App.get_running_app()
		email = self.ids.email.text
		password = self.ids.password.text

		app.auth_service.sign_in(email, password)



