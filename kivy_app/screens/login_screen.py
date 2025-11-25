from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from services.api import backend_login

class LoginScreen(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def do_login(self):
        user = self.ids.email_input.text
        pwd = self.ids.password_input.text

        ok, data = backend_login(user, pwd)

        if ok:
            print("Login correcto:", data)
            self.manager.current = "home"
        else:
            print("Error de login")
