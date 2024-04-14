from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from Screens import *
from Helper_class import *
import subprocess
from tkinter import filedialog

Window.maximize()

class App(MDApp):
    def build (self):
        sm = ScreenManager()
        sm.add_widget(Main_Screen(name ='Main'))
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Red'
        return sm
    #Открытие информации о письме
    def Dialog_open(self, file_path):
        file_path = file_path[6:]
        file_path = file_path.replace("\\", "/")
        if file_path[-4:] == ".eml":
            outlook_path = "C:/Program Files (x86)/Microsoft Office/root/Office16/OUTLOOK.EXE"
            try:
                subprocess.run([outlook_path, file_path])
            except:
                outlook_path = filedialog.askdirectory()
                outlook_path = Path(outlook_path)
                subprocess.run([outlook_path, file_path])
            finally:
                pass


if __name__ == "__main__":
    App().run()
    
    