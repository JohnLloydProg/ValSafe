from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from objects import Message
from kivy.app import App
from fb import Firebase
from kivy.clock import Clock
import threading


class ChatScreen(Screen):
    background_color = [1, 87/255, 87/255, 1]
    font_color = [50/255, 50/255, 50/255, 1]
    user = None
    fb = Firebase()

    def on_enter(self, *args):
        self.app = App.get_running_app()
        self.user = self.app.user
        self.backing = False
        self.chats = []
        self.update = Clock.schedule_interval(self.update_chat, 1)
        self.t = threading.Thread(target=self.get_chat, daemon=True)
        self.t.start()
        return super().on_enter(*args)
    
    def change_gc(self):
        messenger = self.ids['messenger']
        messenger.clear_widgets()
        self.chats.clear()
    
    def get_chat(self):
        while True:
            conversation = self.fb.get_chat(self.ids['username'].text, self.app.user.idToken)
            if conversation:
                conversation = list(reversed(conversation))[:10]
                conversation.reverse()
                for message in conversation:
                    localId = message[0].split('-')[1]
                    message_id = message[0].split('-')[0]
                    user = self.fb.get_user(localId, self.app.user.idToken)
                    if user:
                        if (message_id, user['username'], message[1]) not in self.chats:
                            self.chats.append((message_id, user['username'], message[1]))
            if self.backing:
                break
    
    def update_chat(self, *args):
        messenger = self.ids['messenger']
        self.chats.sort(key=lambda x: x[0])
        children = [chat[0] for chat in self.chats.copy()]
        children = list(reversed(children))[:10]
        children.reverse()
        for chat in self.chats:
            if chat[1] == self.user.infos['username']:
                message = Message(chat[0], chat[1], chat[2], (1, 1, 1, 1))
                if message.id not in messenger.ids:
                    messenger.add_widget(message)
                    messenger.ids[message.id] = message
            else:
                message = Message(chat[0], chat[1], chat[2])
                if message.id not in messenger.ids:
                    messenger.add_widget(message)
                    messenger.ids[message.id] = message
        for messageId in messenger.ids:
            if messageId not in children:
                messenger.remove_widget(messenger.ids[messageId]) 
        
    def back(self):
        self.backing = True
        self.update.cancel()
        self.app.sm.current = 'navigation'


    def chat(self, textinput:TextInput):
        if len(textinput.text) > 0:
            conversation = self.fb.get_chat(self.ids['username'].text, self.app.user.idToken)
            if conversation:
                number = len(conversation)
            else:
                number = 0
            self.fb.post_chat(self.ids['username'].text, textinput.text, str(number), self.app.user.localId, self.app.user.idToken)
            textinput.text = ''
