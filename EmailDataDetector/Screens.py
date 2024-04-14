from kivy.uix.screenmanager import Screen
from Helper_class import List_Item
import os
import re
import email
import PyPDF2
from email import policy
from email.parser import BytesParser
from email.header import decode_header
from tkinter import filedialog
from pathlib import Path
import zipfile
import io
# from ScanQR import process_pdf  # Импортируем функцию для обработки PDF из второго скрипта

#Главный экран
class Main_Screen(Screen):
    # Наборы фильтров для письма
    filters = {
        0: {
            'id': 0,
            'name': 'Accounts',
            'code': '',
            'regex': r'\b(\d{20})\b',
        },
        1: {
            'id': 1,
            'name': 'Cards',
            'code': '',
            'regex': r'\b(\d{16})\b|\b(\d{4} \d{4} \d{4} \d{4})\b'
        },
        2: {
            'id': 2,
            'name': 'Passport',
            'code': '',
            'regex': r'\b(\d{4} \d{6})\b|\b(\d{4} № \d{6})\b|\b(\d{4}-\d{6})\b|\b(\d{4}-\d{6})\b|\b(\d{4}№\d{6})\b|\b(\d{4} N\d{6})\b|\b(\d{2} \d{2} N \d{6})\b|\b(\d{2} \d{2} № \d{6})\b|\b(\d{4} N \d{6})\b|\b(\d{2} \d{2} № \d{6})\b|\b(\d{4} \d{3} № \d{6})\b'
        },
        3: {
            'id': 3,
            'name': 'Phone number',
            'code': '',
            'regex': r'\b(?:\+?7|\b8)(?:\s*[(\-]?\d{3}\)?|\s*\d{3}[-)]?)\s*\d{3}[- ]?\d{2}[- ]?\d{2}\b'
        },
        4: {
            'id': 4,
            'name': 'Snils',
            'code': '',
            'regex': r'\b(\d{3}-\d{3}-\d{3} \d{2})\b'
        },
    }
    processed_data = []
    Account_flag = True
    Card_flag = True
    Passport_flag = True
    Phone_flag = True
    Snils_flag = True
    Qr_code_flag = True
    Not_detected_flag = True
    dataset_dir = None
    count = 0
    leaked_file = False
    

    #Функция для обновления списка
    def update_list(self):
        self.ids.container.clear_widgets()
        for i in range(len(self.processed_data)):
            if str(self.processed_data[i][1][-4:]) == ".eml":
                autor_mail = self.get_sender(self.processed_data[i][1])
                filter_name = self.processed_data[i][0]
                text = self.processed_data[i][2]
                if self.Account_flag and filter_name == "Accounts":
                    text = f"От кого: {autor_mail}{' '*5}Accounts: {text}"
                elif self.Card_flag and filter_name == "Cards":
                    text = f"От кого: {autor_mail}{' '*5}Cards: {text}"
                elif self.Passport_flag and filter_name == "Passport":
                    text = f"От кого: {autor_mail}{' '*5}Passport: {text}"
                elif self.Phone_flag and filter_name == "Phone number":
                    text = f"От кого: {autor_mail}{' '*5}Phone number: {text}"
                elif self.Snils_flag and filter_name == "Snils":
                    text = f"От кого: {autor_mail}{' '*5}Snils: {text}"
                # elif self.Qr_code_flag and filter_name == "Qr":
                #     text = f"От кого: {autor_mail}{' '*5}Qr: {text}"
                # elif self.Not_detected_flag and filter_name == "None":
                #     text = f"От кого: {autor_mail}{' '*5}Конфиденциальных данных не обнаружено"
                else:
                    continue
                mail_number = "File: " + self.processed_data[i][1]
                self.ids.container.add_widget(
                    List_Item(mail_number,text)
                )


    #Функция отображения объектов в списке
    def on_enter(self):
        self.ids.container.clear_widgets() 
        direct_way = filedialog.askdirectory() 
        self.dataset_dir = Path(direct_way) 
        files = self.get_dataset_files(self.dataset_dir) 
 
        for file in files: 
            self.leaked_file = False 
            self.check_str_filter(self.eml_to_text(file), file) 
            self.process_email(file)

        for i in range(len(self.processed_data)):
            if str(self.processed_data[i][1][-4:]) == ".eml":
                # count +=1
                autor_mail = self.get_sender(self.processed_data[i][1])
                filter_name = self.processed_data[i][0]
                text = self.processed_data[i][2]
                if self.Account_flag and filter_name == "Accounts":
                    text = f"От кого: {autor_mail}{' '*5}Accounts: {text}"
                elif self.Card_flag and filter_name == "Cards":
                    text = f"От кого: {autor_mail}{' '*5}Cards: {text}"
                elif self.Passport_flag and filter_name == "Passport":
                    text = f"От кого: {autor_mail}{' '*5}Passport: {text}"
                elif self.Phone_flag and filter_name == "Phone number":
                    text = f"От кого: {autor_mail}{' '*5}Phone number: {text}"
                elif self.Snils_flag and filter_name == "Snils":
                    text = f"От кого: {autor_mail}{' '*5}Snils: {text}"
                # elif self.Qr_code_flag and filter_name == "Qr":
                #     text = f"От кого: {autor_mail}{' '*5}Qr: {text}"
                # elif self.Not_detected_flag and filter_name == "None":
                #     text = f"От кого: {autor_mail}{' '*5}Конфиденциальных данных не обнаружено"
                else:
                    continue
                mail_number = "File: " + self.processed_data[i][1]
                self.ids.container.add_widget(
                    List_Item(mail_number,text)
                )
                
        self.ids.count_mail.text = str(self.count)


    #Переключение флагов с помощью checkbox
    def on_checkbox_active(self, checkbox, value, id):
        if value:
            if id == 'card':
                self.Card_flag = True
            elif id == 'passport':
                self.Passport_flag = True
            elif id == 'phone':
                self.Phone_flag = True
            elif id == 'snils':
                self.Snils_flag = True
            elif id == "qr-code":
                self.Qr_code_flag = True
            elif id == "account":
                self.Account_flag = True
            elif id == "none":
                self.Not_detected_flag = True
        else:
            if id == 'card':
                self.Card_flag = False
            elif id == 'passport':
                self.Passport_flag = False
            elif id == 'phone':
                self.Phone_flag = False
            elif id == 'snils':
                self.Snils_flag = False
            elif id == "qr-code":
                self.Qr_code_flag = False
            elif id == "account":
                self.Account_flag = False
            elif id == "none":
                self.Not_detected_flag = False
        self.update_list()
        

    def get_sender(self,eml_file_path):
        with open(eml_file_path, 'rb') as eml_file:
            eml_msg = eml_file.read()
        msg = str(BytesParser(policy=policy.default).parsebytes(eml_msg))
        sender_mail = re.search(r'X-Sender:\s*(\S+)', msg).group(1)
        return sender_mail
        
    # pdf в текст
    def convert_pdf_to_txt(self, part):
        pdf_data = part.get_payload(decode=True)
        pdf_file = io.BytesIO(pdf_data)

        pdf_reader = PyPDF2.PdfReader(pdf_file)

        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

        return text


    # Получение всех файлов в папке (включая вложенные папки)
    def get_dataset_files(self,dataset_dir):
        files = []

        for item in os.listdir(dataset_dir):
            item_path = os.path.join(dataset_dir, item)

            if os.path.isfile(item_path):
                files.append(item_path)

            elif os.path.isdir(item_path):
                files.extend(self.get_dataset_files(item_path))

        return files
    

    def process_zip_archive(self, filename, part): 
        # Создаем временную папку
        temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
        os.makedirs(temp_dir, exist_ok=True)

        zip_data = io.BytesIO(part.get_payload(decode=True))

        if not zipfile.is_zipfile(zip_data):
            print(f"Skipping non-zip file: {filename}")
            return

        try:
            # Извлекаем содержимое ZIP-архива во временную папку
            with zipfile.ZipFile(zip_data, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # Перебираем файлы во временной папке и обрабатываем их
            for file_name in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file_name)
                self.process_temp_file(file_path, False)

        except RuntimeError as e:
            if 'encrypted' in str(e):
                print(f"Skipping encrypted archive: {filename}")
            else:
                raise  # Re-raise other RuntimeError exceptions

        # Удаляем временную папку после обработки
        for root, dirs, files in os.walk(temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

        os.rmdir(temp_dir)
        
    # eml в text
    def eml_to_text(self,file_path):
        def extract_text(part):
            if part.is_multipart():
                text = ""
                for subpart in part.iter_parts():
                    text += extract_text(subpart)
                return text
            else:
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    try:
                        return part.get_payload(decode=True).decode()
                    except UnicodeDecodeError:
                        pass
                elif content_type == 'message/rfc822':
                    return self.eml_to_text(part.get_filename())
                return ""

        with open(file_path, 'rb') as fp:
            msg = BytesParser(policy=policy.default).parse(fp)

        return extract_text(msg)

    def decode_mime_words(self,s):
        decoded = []
        pieces = decode_header(s)
        for piece, encoding in pieces:
            if encoding:
                piece = piece.decode(encoding)
            decoded.append(piece)
        return ''.join(decoded)

    # Функция для обработки одного электронного письма
    def process_email(self, file):
        with open(file, 'rb') as eml_file:
            msg = BytesParser(policy=policy.default).parse(eml_file)

            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue

                filename = part.get_filename()

                if filename and filename.lower().endswith('.zip'):
                    self.process_zip_archive(filename, part)

                elif (filename and filename.lower().endswith('.pdf')) or (filename and filename.lower().endswith('.txt')):
                    self.process_temp_file(filename, part)
    
    # pdf в текст
    def convert_pdf_to_txt_file(self, pdf_file_path):
        pdf_file = open(pdf_file_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

        pdf_file.close()

        return text
    

    # Обработка внешних файлов
    def process_temp_file(self, filepath, part):
        filename = os.path.basename(filepath)

        if filename.lower().endswith('.pdf'):
            # можно что-то с qr-кодом
            # if part:
            #     pdf_path = save_pdf(part)
            #     qr_images = extract_qr_images_from_pdf(pdf_path)
            #     detect_qr_codes(qr_images)

            if part:
                text = self.convert_pdf_to_txt(part)
                self.check_str_filter(text, filename)
            else:
                self.check_str_filter(self.convert_pdf_to_txt_file(filepath), filename)

        elif filename.lower().endswith('.txt'):
            if part:
                text = part.get_payload(decode=True).decode('utf-16')
                self.check_str_filter(text, filename)
            else:
                with open(filepath, 'r', encoding='utf-16') as txt_file:
                    text = txt_file.read()
                    self.check_str_filter(text, filename)


    # Функция для сохранения PDF-файла из письма и возврата его пути
    def save_pdf(self,pdf_part):
        filename = pdf_part.get_filename()
        with open(filename, 'wb') as f:
            f.write(pdf_part.get_payload(decode=True))
        return filename


    # Проверка через regex на наличие соответствия с фильтром
    def check_str_filter(self, str, file_name):
        self.leaked_file = False

        for filter_name, filter_data in self.filters.items():
            matches = re.finditer(filter_data['regex'], str)
            found_in_file = False

            for match in matches:
                start_index = max(0, match.start())
                end_index = min(len(str), match.end())
                filter_name_retutn = filter_data['name']
                mail_name = file_name
                data = str[start_index:end_index]
                helper_arr = [filter_name_retutn, mail_name, data]
                self.processed_data.append(helper_arr)

                found_in_file = True

            if found_in_file:
                self.leaked_file = True

        if self.leaked_file:
            Main_Screen.count += 1  # Incrementing class variable

        
