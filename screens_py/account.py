from kivy.uix.screenmanager import Screen
from kivy.app import App
from fb import Firebase


class AccountScreen(Screen):
    background_color = [1, 87/255, 87/255, 1]
    font_color = [50/255, 50/255, 50/255, 1]
    fb = Firebase()

    def on_enter(self, *args):
        self.app = App.get_running_app()
        user = self.app.user
        infos = {
            'password': self.ids['password'], 'confirm password': self.ids['confirm_password'], 
            'full name': self.ids['full_name'], 'username': self.ids['username'], 
            'email': self.ids['email'], 'sex': self.ids['sex'], 'contact no': self.ids['contact_no'], 
            'birthdate': self.ids['birthdate'], 'age': self.ids['age'], 'address': self.ids['address'], 
            'health concerns': self.ids['health_concerns'], 'blood type': self.ids['blood_type'], 'emergency name': self.ids['emergency_name'], 
            'relationship': self.ids['relationship'], 'emergency address': self.ids['emergency_address'], 'emergency contact no': self.ids['emergency_contact_no']
        }
        for key in infos.keys():
            infos[key].text = user.infos[key]
        return super().on_enter(*args)

    def save(self):
        infos = {
            'password': self.ids['password'].text, 'confirm password': self.ids['confirm_password'].text, 
            'full name': self.ids['full_name'].text, 'username': self.ids['username'].text, 
            'email': self.ids['email'].text, 'sex': self.ids['sex'].text, 'contact no': self.ids['contact_no'].text, 
            'birthdate': self.ids['birthdate'].text, 'age': self.ids['age'].text, 'address': self.ids['address'].text, 
            'health concerns': self.ids['health_concerns'].text, 'blood type': self.ids['blood_type'].text, 'emergency name': self.ids['emergency_name'].text, 
            'relationship': self.ids['relationship'].text, 'emergency address': self.ids['emergency_address'].text, 'emergency contact no': self.ids['emergency_contact_no'].text
        }
        reply = self.fb.post_infos(infos, self.app.user.localId, self.app.user.idToken)
        self.app.sm.current = 'navigation'
