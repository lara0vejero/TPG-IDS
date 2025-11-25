from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, FadeTransition

from screens.login_screen import LoginScreen
from screens.home_screen import HomeScreen


class MainScreenManager(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        Builder.load_file("app.kv")

        sm = MainScreenManager(transition=FadeTransition())
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(HomeScreen(name="home"))

        sm.current = "login"
        return sm

if __name__ == "__main__":
    MainApp().run()
