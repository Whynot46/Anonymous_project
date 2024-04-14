from email import policy
from email.parser import BytesParser
import re
import os
from tkinter import filedialog
from pathlib import Path
from queue import Queue

# Словарь конфиденциальных данных
class_dir = {0: "nothing", 1: "account", 2:"card", 3:"passport", 4:"phone", 5:"snils", 6:"qr"}

# Принимает .eml и возвращает объект текста сообщения типа string
def eml_to_text(eml_file_path):
    with open(eml_file_path, 'rb') as eml_file:
        eml_msg = eml_file.read()

    msg = BytesParser(policy=policy.default).parsebytes(eml_msg)
    string = msg.get_payload(decode=True).decode()

    return string


# Принимает .eml и сохраняет его в формате .txt
i = 0
def save_eml_as_txt(eml_file_path, class_id):
    with open(eml_file_path, 'rb') as fp:
        eml = fp.read()

    msg = BytesParser(policy=policy.default).parsebytes(eml)
    body = msg.get_payload(decode=True).decode()

    with open(f"data/{class_dir[class_id]}/{class_dir[class_id]}_{i}.txt", "w") as txt_file:
        txt_file.write(body)
    
    i+=1

# Принимает .eml и возвращает объект отправителя типа string
def get_sender(eml_file_path):
    with open(eml_file_path, 'rb') as eml_file:
        eml_msg = eml_file.read()
    msg = str(BytesParser(policy=policy.default).parsebytes(eml_msg))
    sender_mail = re.search(r'X-Sender:\s*(\S+)', msg).group(1)
    return sender_mail


# Получает пути всех файлов в директорииdef get_file_paths():
def get_file_paths():
    direct_way = filedialog.askdirectory()
    direct = Path(direct_way)
    queue = Queue(100)

    for root, dirs, files in os.walk(direct):
        for file in files:
            file_path = os.path.join(root, file)
            queue.put(file_path)

    return queue.queue