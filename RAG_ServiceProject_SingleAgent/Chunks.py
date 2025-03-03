from langchain_text_splitters import RecursiveCharacterTextSplitter

class Chunks:
    def __init__(self, documents):
        documents = self.documents

# Chunk 생성
def generate_chunk(documents):
    """

    Args:
        documents (List): pdf, ppt 데이터 

    Returns:
        chunks: chunk 생성 
    """
    text_splitter = RecursiveCharacterTextSplitter( 
                chunk_size=1000,  # Maximum size of each chunk
                chunk_overlap=100,  # Number of overlapping characters between chunks
            )

    

    chunks = text_splitter.split_documents(documents)
    
    return chunks