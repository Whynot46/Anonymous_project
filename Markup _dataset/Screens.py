from kivy.uix.screenmanager import Screen
from email import policy
from email.parser import BytesParser
import re
import os
from tkinter import filedialog
from pathlib import Path
from queue import Queue

#Главный экран
class Main_Screen(Screen):
    # Словарь конфиденциальных данных
    class_dir = {0: "nothing", 1: "account", 2:"card", 3:"passport", 4:"phone", 5:"snils", 6:"qr"}
    count = 0
    eml_queue = None
    eml_file_path = ''

    # Принимает .eml и возвращает объект текста сообщения типа string
    def eml_to_text(self,file_path):
        with open(file_path, 'rb') as fp:
            eml = fp.read()

        msg = BytesParser(policy=policy.default).parsebytes(eml)

        if msg.is_multipart():
            for part in msg.walk():
                content_disposition = str(part.get("Content-Disposition"))
                try:
                    body = part.get_payload(decode=True).decode('utf-8', 'ignore')
                except:
                    pass
        else:
            body = msg.get_payload(decode=True).decode('utf-8', 'ignore')

        return re.sub(r"<[^>]+>", "", body, flags=re.S)

    # Принимает .eml и сохраняет его в формате .txt
    def save_eml_as_txt(self,eml_file_path, class_id):
        with open(eml_file_path, 'rb') as fp:
            eml = fp.read()

        msg = BytesParser(policy=policy.default).parsebytes(eml)

        if msg.is_multipart():
            for part in msg.walk():
                content_disposition = str(part.get("Content-Disposition"))
                try:
                    body = part.get_payload(decode=True).decode()
                except:
                    pass
        else:
            body = msg.get_payload(decode=True).decode()

        if body is not None:
            with open(f"data/{self.class_dir[class_id]}/{self.class_dir[class_id]}_{self.count}.txt", "w") as txt_file:
                txt_file.write(body)
            
            self.count+=1
            self.on_enter()

    # Принимает .eml и возвращает объект отправителя типа string
    def get_sender(self,eml_file_path):
        with open(eml_file_path, 'rb') as eml_file:
            eml_msg = eml_file.read()
        msg = str(BytesParser(policy=policy.default).parsebytes(eml_msg))
        sender_mail = re.search(r'X-Sender:\s*(\S+)', msg).group(1)
        return sender_mail
    
    # Получает пути всех файлов в директорииdef get_file_paths():
    def get_file_paths(self):
        direct_way = filedialog.askdirectory()
        direct = Path(direct_way)
        queue = Queue(100)

        for root, dirs, files in os.walk(direct):
            for file in files:
                file_path = os.path.join(root, file)
                queue.put(file_path)

        return queue.queue
    
    def check_dir(self):
        for data_id in self.class_dir:
            if not os.path.exists(f"data/{self.class_dir[data_id]}"):
                os.makedirs(f"data/{self.class_dir[data_id]}")
    
    #Вывод даных из файла на экран
    def on_enter(self):
        self.check_dir()
        if self.count == 0:
            self.eml_queue = self.get_file_paths()
        self.eml_file_path = self.eml_queue.pop()
        self.ids.mail_text.text = f"[color=000000]{self.eml_to_text(self.eml_file_path)}[/color]"
        self.ids.autor_mail.text = f"[color=000000]Отправитель: {self.get_sender(self.eml_file_path)}[/color]"
        
        
        


        
