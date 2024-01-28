from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.app import App
from fb import Firebase
from objects import User


class RegisterScreen(Screen):
    background_color = [1, 87/255, 87/255, 1]
    font_color = [50/255, 50/255, 50/255, 1]
    popup = Popup(
        title = 'Information About ValSafe',
        content = Label(
            text = 'ValSafe is a blank'
        ), 
        size_hint = (0.8, None), 
        height = 400
    )
    fb = Firebase()

    def on_enter(self, *args):
        self.app = App.get_running_app()
        infos = {
            'password': self.ids['password'], 'confirm password': self.ids['confirm_password'], 
            'full name': self.ids['full_name'], 'username': self.ids['username'], 
            'email': self.ids['email'], 'sex': self.ids['sex'], 'contact no': self.ids['contact_no'], 
            'birthdate': self.ids['birthdate'], 'age': self.ids['age'], 'address': self.ids['address'], 
            'health concerns': self.ids['health_concerns'], 'blood type': self.ids['blood_type'], 'emergency name': self.ids['emergency_name'], 
            'relationship': self.ids['relationship'], 'emergency address': self.ids['emergency_address'], 'emergency contact no': self.ids['emergency_contact_no']
        }
        if self.app.testing:
            infos['password'].text = '123456789'
            infos['confirm password'].text = '123456789'
            infos['full name'].text = 'John Lloyd Unida'
            infos['username'].text = 'unids'
            infos['email'].text = 'johnlloydunida0@gmail.com'
            infos['sex'].text = 'Male'
            infos['contact no'].text = '09613372575'
            infos['birthdate'].text = 'September 27, 2004'
            infos['age'].text = '18'
            infos['address'].text = 'Assumption Ville.'
            infos['health concerns'].text = 'None'
            infos['blood type'].text = 'AB+'
            infos['emergency name'].text = 'Marilou Unida'
            infos['relationship'].text = 'Parent'
            infos['emergency address'].text = 'Assumption Ville.'
            infos['emergency contact no'].text = '09321312321'

        return super().on_enter(*args)
    
    def tick(self, widget, value):
        print(widget, value)

    def check(self):
        infos = {
            'password': self.ids['password'].text, 'confirm password': self.ids['confirm_password'].text, 
            'full name': self.ids['full_name'].text, 'username': self.ids['username'].text, 
            'email': self.ids['email'].text, 'sex': self.ids['sex'].text, 'contact no': self.ids['contact_no'].text, 
            'birthdate': self.ids['birthdate'].text, 'age': self.ids['age'].text, 'address': self.ids['address'].text, 
            'health concerns': self.ids['health_concerns'].text, 'blood type': self.ids['blood_type'].text, 'emergency name': self.ids['emergency_name'].text, 
            'relationship': self.ids['relationship'].text, 'emergency address': self.ids['emergency_address'].text, 'emergency contact no': self.ids['emergency_contact_no'].text
        }
        errors = []
        for info in infos.values():
            if len(info) == 0:
                errors.append('i == 0')
                break
        if infos['password'] != infos['confirm password']:
            errors.append('p&cp !=')
        if errors:
            popup = Popup(
                title = 'Registration Error',
                size_hint = (0.8, None), 
                height = 400
            )
            message = ''
            for error in errors:
                if error == 'i == 0':
                    message += 'Please fill up all of the entries.\n'
                if error == 'p&cp !=':
                    message += 'Confirm Password and Password is not the same. \n'
            popup.content = Label(text=message)
            popup.open()
        else:
            try:
                reply = self.fb.sign_up(infos['email'], infos['password'])
                self.fb.post_infos(infos, reply['localId'], reply['idToken'])
                self.app.user = User(reply['localId'], reply['idToken'], infos)
                self.app.sm.current = 'navigation'
            except:
                register_popup = Popup(
                    title = 'Registration Error',
                    size_hint = (0.8, None),
                    content = Label(text='The email you provided is already connected to an account.'), 
                    height = 400
                )
                register_popup.open()
