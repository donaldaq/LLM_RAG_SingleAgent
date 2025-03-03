class Document_ppt:
    def __init__(self, metadata, page_content):
        self.metadata = metadata
        self.page_content = page_content
    
    def __repr__(self):
        return f"Document(metadata={self.metadata}, page_content='{self.page_content[:]}')"

def create_document_list(source, num_pages, page_contents):
    """_summary_

    Args:
        source (String): 소스 데이터 
        num_pages (String): 페이지 넘버 
        page_contents (String): 텍스트 데이터 

    Returns:
        _type_: _description_
    """
    documents = []
    
    for page in range(num_pages):
        metadata = {
            "source": source,
            "page": page,
            "page_label": str(page + 1)  # 페이지 번호를 1부터 시작하도록 설정
        }
        
        # 페이지별 내용이 제공되지 않으면 빈 문자열 사용
        content = page_contents[page] if page_contents and page < len(page_contents) else ""
        
        documents.append(Document_ppt(metadata, content))
    
    return documents