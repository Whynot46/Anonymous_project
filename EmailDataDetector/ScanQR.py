import fitz
from pyzbar.pyzbar import decode
from PIL import Image, ImageChops
import io
import os

def extract_qr_images_from_pdf(pdf_path):
    qr_images = []

    # Открываем PDF
    pdf_document = fitz.open(pdf_path)

    for page_number in range(len(pdf_document)):
        # Получаем страницу
        page = pdf_document.load_page(page_number)
        # Получаем изображения на странице
        images = page.get_images(full=True)

        for img_index, img_info in enumerate(images):
            # Получаем изображение
            xref = img_info[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            # Конвертируем в объект изображения Pillow
            image = Image.open(io.BytesIO(image_bytes))
            # Инвертируем изображение
            inverted_image = ImageChops.invert(image)
            # Сохраняем изображение временно
            image_path = f"./EmailDataDetector/temp_image_{page_number}_{img_index}.png"
            inverted_image.save(image_path)
            qr_images.append(image_path)

    return qr_images

def detect_qr_codes(qr_images):
    for image_path in qr_images:
        # Загружаем изображение и декодируем QR-код
        decoded_objects = decode(Image.open(image_path))
        print(decoded_objects)
        if decoded_objects:
            print("QR code detected:", decoded_objects[0].data.decode())
        else:
            print("QR code not detected")
        
        # Удаление временного файла изображения
        os.remove(image_path)
        