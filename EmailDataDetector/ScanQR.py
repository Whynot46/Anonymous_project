import cv2
from pyzbar.pyzbar import decode
import os.path
from pdf2image import convert_from_path

def extract_images_from_pdf(pdf_path):
    images = []
    pages = convert_from_path(pdf_path)
    for page_num, img in enumerate(pages):
        image_path = f"page{page_num}.png"
        img.save(image_path, 'PNG')
        images.append(image_path)
    return images

def scan_qr_codes(images):
    qr_codes = []
    for image_path in images:
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        qr_codes_data = decode(gray)
        for qr_code_data in qr_codes_data:
            qr_data = qr_code_data.data.decode("utf-8")
            qr_codes.append(qr_data)
    return qr_codes

def process_pdf(pdf_file_path):
    temp_images = extract_images_from_pdf(pdf_file_path)
    qr_codes = scan_qr_codes(temp_images)

    if not qr_codes:
        print("В", pdf_file_path,"нет QR-кодов")
    else:
        print("В", pdf_file_path,"присутствует QR-код")

    # Удаляем временные изображения
    for image_path in temp_images:
        os.remove(image_path)
