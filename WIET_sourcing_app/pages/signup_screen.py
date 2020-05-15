import threading

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.behaviors import MagicBehavior
from kivymd.uix.button import MDRectangleFlatButton
from kivy.uix.button import Button
from kivymd.uix.snackbar import Snackbar

from WIET_sourcing_app.services.auth_service import AuthService


class MagicButton(MagicBehavior, MDRectangleFlatButton):
    pass


class SignupScreen(Screen):

    def validate(self, *args):
        text_field_error = args[0]
        message = AuthService.password_check(text_field_error.text)
        if not message == 'OK':
            text_field_error.error = True
            self.ids.password.helper_text = message
        else:
            text_field_error.error = False

    def move_to_login(self):
        app = App.get_running_app()
        app.change_screen("login_screen", "backward")

    def sign_up(self):
        threading.Thread(target=self.sign_up_worker).start()

    def sign_up_worker(self):
        app = App.get_running_app()
        name = self.ids.name.text
        email = self.ids.email.text
        password = self.ids.password.text
        if not app.auth_service.sign_up(name, email, password):
            Snackbar(text="Failed to sign up!").show()
            self.ids['button_one'].md_bg_color = app.theme_cls.error_color
            self.ids['button_one'].text_color = app.theme_cls.accent_color
