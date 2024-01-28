from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from objects import NumberButton
from kivy.app import App
from plyer import call


class HotlineScreen(Screen):
    background_color = [1, 87/255, 87/255, 1]
    font_color = [50/255, 50/255, 50/255, 1]
    number = '+63'
    hotlines = {
        'Valenzuela City Police':'8352-4000', 
        'Bureau of Fire Protection':'8352-3000', 
        'Valenzuela City Emergency Hospital':'8352-6000',
        'Valenzuela Medical Center': '8294-67-11', 
        'Traffic Management Office': '8352-2000', 
        'Valenzuela Rescue Team': '8292-1405', 
        'Philippine Red Cross': '3432-0273'
    }

    def number_clicked(self, btn:NumberButton):
        name_label = self.ids['caller_name']
        name_label.text = btn.text

    def on_enter(self, *args):
        self.app = App.get_running_app()
        layout = self.ids['caller_numbers']
        layout.clear_widgets()
        for hotline in self.hotlines.keys():
            button = NumberButton(text=hotline)
            button.bind(on_press=self.number_clicked)
            layout.add_widget(button)
        return super().on_enter(*args)
    
    def digit_clicked(self, btn):
        self.number += btn.text
        name_label = self.ids['caller_name']
        name_label.text = self.number

    def back_clicked(self):
        name_label = self.ids['caller_name']
        if name_label.text in self.hotlines.keys():
            name_label.text = '+63'
        elif len(self.number) > 3:
            self.number = self.number[:-1]
        name_label.text = self.number

    def calling(self):
        name_label = self.ids['caller_name']
        if name_label.text in self.hotlines.keys():
            num = self.hotlines[name_label.text]
        else:
            num = name_label.text
        call.makecall(num)
