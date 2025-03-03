import os
from pinecone import Pinecone, ServerlessSpec
PINECONE_API_KEY = "input_your_key"
pc = Pinecone(
    api_key=os.environ.get("PINECONE_API_KEY") or PINECONE_API_KEY
)
class DeleteVectorStore:
    def __init__():
        pass
def delete_index_with_same_name(index_name): 
    """_summary_
        기존에 있는 벡터스토어를 다시 만들 때 삭제하고 다시 만든다. 

    Args:
        index_name (String): vector 인덱스명
    """
    # Delete index if any incdexes of the same name are present
    if index_name in pc.list_indexes().names():
        print(f'Deleting the {index_name} vector database')
        pc.delete_index(index_name)