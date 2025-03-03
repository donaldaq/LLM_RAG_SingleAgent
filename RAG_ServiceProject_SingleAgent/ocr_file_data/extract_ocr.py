import os
import pytesseract as pt
from PIL import Image

# ✅ Tesseract 실행 경로 (Windows 사용 시 필요)
pt.tesseract_cmd = '/usr/local/Cellar/tesseract/5.5.0/bin/tesseract' #TesseractNotFoundError: tesseract is not installed or it's not in your PATH. See README file for more information. 에러 메시지 나올 경우

# ✅ OCR을 수행할 이미지가 있는 폴더 및 저장할 파일
IMAGE_FOLDER = "/opt/homebrew/Cellar/tesseract/5.5.0/bin/images"  # 이미지가 있는 폴더 경로
OUTPUT_FILE = "ocr_result.txt"  # 결과 저장 파일명
LANGUAGE = "kor+eng"  # 한국어+영어 OCR (언어 변경 가능)

def perform_ocr(image_path):
    """이미지에서 Tesseract OCR을 사용하여 텍스트 추출"""
    try:
        img = Image.open(image_path)
        text = pt.image_to_string(img, lang=LANGUAGE)
        return text.strip()
    except Exception as e:
        print(f"❌ Error processing {image_path}: {e}")
        return ""

def process_images(folder_path, output_file):
    """폴더 내 모든 이미지에서 OCR을 수행하고 결과를 저장"""
    with open(output_file, "w", encoding="utf-8") as out_file:
        for filename in sorted(os.listdir(folder_path)):  # 정렬하여 순차 처리
            file_path = os.path.join(folder_path, filename)
            ext = os.path.splitext(filename)[-1].lower()

            # ✅ 지원하는 이미지 파일 확장자
            if ext in [".jpg", ".jpeg", ".png", ".tiff", ".bmp", ".gif"]:
                print(f"Processing: {filename}...")
                extracted_text = perform_ocr(file_path)

                # ✅ OCR 결과 저장
                out_file.write(f"\n\n==== {filename} ====\n{extracted_text}\n")

# ✅ 실행
process_images(IMAGE_FOLDER, OUTPUT_FILE)
print(f"\n✅ OCR processing complete! Text saved in {OUTPUT_FILE}")