from kivy.uix.screenmanager import Screen
from objects import Barangay
from kivy.app import App
import fb


class ReliefScreen(Screen):
    background_color = [1, 87/255, 87/255, 1]
    font_color = [50/255, 50/255, 50/255, 1]

    def on_enter(self, *args):
        self.app = App.get_running_app()
        self.fb = fb.Firebase()
        barangays = self.fb.get_relief_operations(self.app.user.idToken)
        layout = self.ids['barangays']
        layout.clear_widgets()
        for key, value in barangays.items():
            layout.add_widget(Barangay(text=f'{key} - {value}'))
        return super().on_enter(*args)

