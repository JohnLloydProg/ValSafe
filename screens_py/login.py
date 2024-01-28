from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.app import App
from objects import User
from fb import Firebase
import random

class LogInScreen(Screen):
    background_color = [1, 87/255, 87/255, 1]
    font_color = [50/255, 50/255, 50/255, 1]
    info_popup = Popup(
        title = 'Information About ValSafe',
        content = Label(
            text = 'ValSafe is a blank'
        ), 
        size_hint = (0.8, None), 
        height = 400
    )
    facts = [
        'More than half of Americans have not prepared copies of crucial documents.', 
        '48 percent of Americans lack emergency supplies for use in the event of a disaster.', 
        'More than half of parents do not have a designated meeting place in case of a disaster.', 
        '42 percent of cell phone owners do not know all their immediate family members phone numbers.', 
        'Serious Symptoms? Do not Drive. Call 911.'
    ]
    fb = Firebase()

    def on_enter(self, *args):
        self.app = App.get_running_app()
        fact = self.ids['facts']
        fact.text = random.choice(self.facts)
        if self.app.testing:
            self.ids['email'].text = 'johnlloydunida0@gmail.com'
            self.ids['password'].text = '123456789'
        return super().on_enter(*args)

    def remember(self, state:str):
        image = self.ids['toggle_image']
        if state == 'normal':
            image.source = './images/untick-square.png'
        else:
            image.source = './images/tick-square.png'

    def sign_in(self):
        email = self.ids['email'].text
        password = self.ids['password'].text
        try:
            reply = self.fb.sign_in(email, password)
            infos = self.fb.get_infos(reply['localId'], reply['idToken'])
            self.user = User(reply['localId'], reply['idToken'], infos)
            self.app.user = self.user
            self.app.sm.current = 'navigation'
        except Exception as e:
            print(e)
            login_popup = Popup(
                title = 'Log In Failed',
                content = Label(
                    text = 'Email or Password is Wrong!'
                ), 
                size_hint = (0.8, None), 
                height = '200dp'
            )
            login_popup.open()
    
    def info_pop(self):
        self.info_popup.open()
