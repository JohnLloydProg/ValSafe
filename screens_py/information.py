from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.app import App
from objects import CategoriesButton, Information
import os

def clicked(instance):
    app = App.get_running_app()
    app.sm.current = 'topic'
    app.topic_to_show = instance.text

class LobbyScreen(Screen):
    background_color = [1, 87/255, 87/255, 1]
    font_color = [50/255, 50/255, 50/255, 1]

    def on_enter(self, *args):
        self.app = App.get_running_app()
        return super().on_enter(*args)

    def information_clicked(self, btn:Button):
        self.app.sm.current = 'information'
        self.app.info_to_show = btn.text


class InformationScreen(Screen):
    background_color = [1, 87/255, 87/255, 1]
    font_color = [50/255, 50/255, 50/255, 1]
    def on_pre_leave(self, *args):
        self.ids['info_title'].text = 'Loading'
        return super().on_pre_leave(*args)
    def on_enter(self, *args):
        self.app = App.get_running_app()
        info = self.app.info_to_show
        self.ids['info_title'].text = info
        self.ids['image'].source = f'./images/{self.app.info_to_show}-img.jpg'
        layout = self.ids['basic_infos']
        layout.clear_widgets()
        for topic in os.listdir(f'./information/{self.app.info_to_show}'):
            button = CategoriesButton(text=topic.replace('_', ' ').removesuffix('.txt'))
            button.bind(on_press=clicked)
            layout.add_widget(button)
        return super().on_enter(*args)

class TopicScreen(Screen):
    background_color = [1, 87/255, 87/255, 1]
    font_color = [50/255, 50/255, 50/255, 1]
    def on_pre_leave(self, *args):
        self.ids['info_scroll'].scroll_y = 1
        return super().on_pre_leave(*args)
    def on_enter(self, *args):
        self.app = App.get_running_app()
        topic = self.app.topic_to_show
        self.ids['topic_title'].text = topic
        layout = self.ids['information_layout']
        layout.clear_widgets()
        topic = topic.replace(' ', '_')
        with open(f'./information/{self.app.info_to_show}/{topic}.txt', 'r') as f:
            description = f.readlines()
            informations = []
            subtopic = ''
            for line in description:
                if line[0] == '#':
                    layout.add_widget(Information(subtopic, ''.join(informations)))
                    informations.clear()
                    subtopic = ''
                elif line[0] == '$':
                    subtopic = line[1:]
                else:
                    if informations:
                        informations.append(line)
                    else:
                        if len(line) > 2:
                            informations.append(line)
        return super().on_enter(*args)
