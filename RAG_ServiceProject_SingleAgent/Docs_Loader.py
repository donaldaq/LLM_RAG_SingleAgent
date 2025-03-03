# DOCX - Check Path ald Load .pdf .pptx .txt

import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders import UnstructuredPowerPointLoader
from pdf.PineconePDFExtractor import PdfProcessor
from langchain.chains import RetrievalQA
from langchain.schema import Document

from PPTX_Metadata import create_document_list

class Docs_Loader:
    def __init__(self, path, filepath, docs):

        path = self.path
        filepath = self.filepath 
        docs = self.docs

def process_metadata(filepath, docs):

    """

    Args:
        filepath (String): 파일경로명 
        docs (List): 문서데이터 

    Returns:
        pdf_page_data, pdf_page_label_data, page_content_data(String): 데이터 문서 정보 
    """

    
    ppt_page_data = ""
    ppt_page_label_data = ""
    page_content_data =""
    end = " '), "

    # 데이터 로드
    page_list = docs[0].page_content.replace("\n\n\n", "|*|")
    page_list = page_list.split('|*|')
    
    # 페이지 및 데이터 처리
    for i,value in enumerate(page_list,start = 1):
        
        j = i-1
        
        if j < 0:
            j = 0
        
        ppt_page_data += "'page': {}".format(j)+ '_*_'
        ppt_page_label_data += "'page_label': {}".format(i) +'_*_'
        page_content_data += "{}".format(value) + "_*_"
    
    # 리스트 생성 
    ppt_page_data = ppt_page_data.split('_*_')
    ppt_page_label_data = ppt_page_label_data.split('_*_')
    page_content_data = page_content_data.split('_*_')
    
    return ppt_page_data, ppt_page_label_data, page_content_data


def check_and_load_pdf_from_dir(directory):
    """

    Args:
        directory (String): 디렉토리 경로 

    Returns:
        total_documents: pdf, ppt 통합 텍스트 데이터 
    """
    # Ensure the directory path exists
    if not os.path.exists(directory):
        print("Directory does not exist.")
        return False

    # Check if directory is actually a directory
    if not os.path.isdir(directory):
        print("The specified path is not a directory.")
        return False

    # List all files in the directory
    all_files = os.listdir(directory)
    print(f'.pdf,pptx files within the /docs directory: {all_files}')
    
    # Check if each file ends with .docx
    for file in all_files:
        if not file.endswith(".pdf") and not file.endswith(".pptx"):
            print(f"Non-Docs file found: {file}")
            return False
        

# load directory path
    directory_path = directory
    # batch size 
    extractor = PdfProcessor(200)
    # add list comprehension for file os.path.join usage
    pdf_files = [f for f in all_files if f.endswith(".pdf")]
    ppt_files = [f for f in all_files if f.endswith(".pptx")]
    # Create emptly list container
    documents = []
    documents_pdf = []
    documents_pptx = []
    # Loop through the directory, bundle and load docx files. 
    for pdf_file in pdf_files:
        file_path = os.path.join(directory_path, pdf_file)
        pdf_loader = PyPDFLoader(file_path)
        documents_pdf = pdf_loader.load()
        
    for ppt_file in ppt_files:
        file_path = os.path.join(directory_path, ppt_file)
        loader = UnstructuredPowerPointLoader(file_path)
        docs = loader.load()
        pptx_loader = docs[0].page_content
        ppt_page_data, ppt_page_label_data, page_content_data = process_metadata(file_path, docs) 
        document_list = create_document_list(file_path, len(ppt_page_data), page_content_data)
        
        documents_pptx = document_list

        total_documents = documents_pdf+documents_pptx



    return total_documents