import kivy as kv
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from screens_py.login import LogInScreen
from screens_py.register import RegisterScreen
from screens_py.navigation import NavigationScreen
from screens_py.information import LobbyScreen, InformationScreen, TopicScreen
from screens_py.hotline import HotlineScreen
from screens_py.account import AccountScreen
from screens_py.chat import ChatScreen
from screens_py.relief import ReliefScreen
from kivy.utils import platform
import threading
from fb import Firebase
from time import sleep
if platform == 'android':
    from android.permissions import request_permissions, Permission
    from jnius import autoclass
    request_permissions([
        Permission.CALL_PHONE, Permission.INTERNET, 
        Permission.ACCESS_FINE_LOCATION, Permission.ACCESS_COARSE_LOCATION
        ])

Builder.load_file('./screens_kv/login.kv')
Builder.load_file('./screens_kv/register.kv')
Builder.load_file('./screens_kv/navigation.kv')
Builder.load_file('./screens_kv/information.kv')
Builder.load_file('./screens_kv/hotline.kv')
Builder.load_file('./screens_kv/account.kv')
Builder.load_file('./screens_kv/chat.kv')
Builder.load_file('./screens_kv/relief.kv')


class ValSafeApp(MDApp, App):
    sm = ScreenManager()
    info_to_show = ''
    topic_to_show = ''
    emergency_mode = False
    user = None
    testing = False
    closing = False
    fb = Firebase()

    def build(self):
        self.login_screen = LogInScreen(name='log in')
        self.sm.add_widget(self.login_screen)
        self.register_screen = RegisterScreen(name='register')
        self.sm.add_widget(self.register_screen)
        self.navigation_screen = NavigationScreen(name='navigation')
        self.sm.add_widget(self.navigation_screen)
        self.lobby_screen = LobbyScreen(name='lobby')
        self.sm.add_widget(self.lobby_screen)
        self.information_screen = InformationScreen(name='information')
        self.sm.add_widget(self.information_screen)
        self.hotline_screen = HotlineScreen(name='hotline')
        self.sm.add_widget(self.hotline_screen)
        self.account_screen = AccountScreen(name='account')
        self.sm.add_widget(self.account_screen)
        self.chat_screen = ChatScreen(name='chat')
        self.sm.add_widget(self.chat_screen)
        self.topic_screen = TopicScreen(name='topic')
        self.sm.add_widget(self.topic_screen)
        self.relief_screen = ReliefScreen(name='relief')
        self.sm.add_widget(self.relief_screen)
        self.sm.current = 'log in'
        return self.sm
    
    def on_start(self):
        self.update = threading.Thread(target=self.get_update)
        self.update.start()
        return super().on_start()

    def on_stop(self):
        self.closing = True
        return super().on_stop()
    
    def get_update(self):
        while True:
            if self.user:
                emergency_mode = self.fb.get_emergency_mode(self.user.idToken)
                if emergency_mode == 'false':
                    self.emergency_mode = False
                else:
                    self.emergency_mode = True
            if self.closing:
                break
            sleep(1)


if __name__ == '__main__':
    ValSafeApp().run()
