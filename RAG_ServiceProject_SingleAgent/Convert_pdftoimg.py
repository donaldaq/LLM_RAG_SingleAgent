import fitz  # PyMuPDF
import io
import os
from PIL import Image

# 'fitz_image' 폴더가 없으면 새로 생성
output_folder = "fitz_image"
file_name = "pdf_file2.pdf"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


# 파일
pdf_file = fitz.open(file_name)

# pdf pages
for page_index in range(len(pdf_file)):
    
    page = pdf_file[page_index]

    # 페이지 리스트 
    image_list = page.get_images(full=True)

    # 페이지에서 넘버 확인
    if image_list:
        print(f"[+] Found a total of {len(image_list)} images in page {page_index + 1}")
    # else:
    #     print("[!] No images found on page", page_index + 1)

    # 페이지에서 이미지 추출
    for image_index, img in enumerate(image_list, start=1):
        xref = img[0]
        base_image = pdf_file.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]

        # 파일 저장 
        image_filename = f"{output_folder}/page_{page_index + 1}_image_{image_index}.{image_ext}"
        with open(image_filename, "wb") as img_file:
            img_file.write(image_bytes)


pdf_file.close()