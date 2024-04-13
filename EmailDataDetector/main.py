from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from Screens import *
from Helper_class import *

Window.maximize()

class App(MDApp):
    def build (self):
        sm = ScreenManager()
        sm.add_widget(Main_Screen(name ='Main'))
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Red'
        return sm
    #Открытие информации о письме
    def Dialog_open(self,id):
        print(f"Открыто {id}")
if __name__ == "__main__":
    App().run()
    
    