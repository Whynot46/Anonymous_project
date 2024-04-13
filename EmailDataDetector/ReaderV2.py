import os
import re
import email
import PyPDF2
from email import policy
from email.parser import BytesParser
from email.header import decode_header
from ScanQR import process_pdf  # Импортируем функцию для обработки PDF из второго скрипта
from tkinter import filedialog
from pathlib import Path
# Путь к папке с файлами письма
direct_way = filedialog.askdirectory()
dataset_dir = Path(direct_way)

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


def convert_pdf_to_txt(pdf_file_path):
    pdf_file = open(pdf_file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

    pdf_file.close()

    return text


# Функция для извлечения PDF из электронного письма и обработки их вторым скриптом
def process_emails(dataset_dir):
    files = get_dataset_files(dataset_dir)

    for file in files:
        print(f"Processing {file}")
        process_email(file)

# Получение всех файлов в папке (включая вложенные папки)
def get_dataset_files(dataset_dir):
    files = []

    for item in os.listdir(dataset_dir):
        item_path = os.path.join(dataset_dir, item)

        if os.path.isfile(item_path):
            files.append(item_path)

        elif os.path.isdir(item_path):
            files.extend(get_dataset_files(item_path))

    return files

# eml в text
def eml_to_text(file_path):
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
                return eml_to_text(part.get_filename())
            return ""

    with open(file_path, 'rb') as fp:
        msg = BytesParser(policy=policy.default).parse(fp)

    return extract_text(msg)

def decode_mime_words(s):
    decoded = []
    pieces = decode_header(s)
    for piece, encoding in pieces:
        if encoding:
            piece = piece.decode(encoding)
        decoded.append(piece)
    return ''.join(decoded)



# Функция для обработки одного электронного письма
def process_email(eml_file_path):
    with open(eml_file_path, 'rb') as eml_file:
        msg = BytesParser(policy=policy.default).parse(eml_file)

        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()

            if filename and filename.lower().endswith('.pdf'):
                pdf_path = save_pdf(part)
                # qr_codes = process_pdf(pdf_path) #можно что-то с qr-кодом
                check_str_filter(convert_pdf_to_txt(filename), filename)

                # Удаляем сохраненный PDF-файл после обработки
                os.remove(pdf_path)

            elif filename and filename.lower().endswith('.txt'):
                try:
                    text = part.get_payload(decode=True).decode('utf-16')  # Декодируем текстовый файл
                    check_str_filter(text, filename)
                except UnicodeDecodeError:
                    pass

# Функция для сохранения PDF-файла из письма и возврата его пути
def save_pdf(pdf_part):
    filename = pdf_part.get_filename()
    with open(filename, 'wb') as f:
        f.write(pdf_part.get_payload(decode=True))
    return filename


# Проверка через regex на наличие соответствия с фильтром
def check_str_filter(str, file_name):
    for filter_name, filter_data in filters.items():
        matches = re.finditer(filter_data['regex'], str)

        for match in matches:
            start_index = max(0, match.start())
            end_index = min(len(str), match.end())

            print('(file - ' + file_name + ' ::: ' + filter_data['name'] + '): ' + str[start_index:end_index] + '\n')


# Вызов функции для обработки электронных писем
files = get_dataset_files(dataset_dir)

for file in files:
    check_str_filter(eml_to_text(file),file)
    process_email(file)
