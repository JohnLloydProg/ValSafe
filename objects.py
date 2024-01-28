from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class User:
    def __init__(self, localId, idToken, infos: dict):
        self.localId = localId
        self.idToken = idToken
        self.infos = infos


class NumberButton(Button):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.color = (1, 1, 1, 1)
        self.text = text
        self.size_hint = (1, None)
        self.height = '50dp'
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.background_active = ''


class CategoriesButton(Button):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.color = (50/255, 50/255, 50/255, 1)
        self.text = text
        self.size_hint = (1, None)
        self.height = '50dp'
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.background_active = ''

class Message(BoxLayout):
    def __init__(self, id, username, message, color=(0, 0, 0, 1), **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.ids['name'].text = username
        self.ids['name'].color = color
        self.ids['message'].text = message

class Information(BoxLayout):
    def __init__(self, topic, description, **kwargs):
        super().__init__(**kwargs)
        self.ids['topic'].text = topic
        self.ids['description'].text = description

class Barangay(Label):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text
