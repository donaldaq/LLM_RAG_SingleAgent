from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
import os
import time

# Pinecone api key 설정
PINECONE_API_KEY = "input_your_key"
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY") or PINECONE_API_KEY)

class Generate_VectorStore:
    def __init__():
        pass


def load_or_create_embeddings_index(index_name, chunks, namespace):
    """

    Args:
        index_name (_type_): Pinecone 인덱스 
        chunks (_type_): 생성된 chunk
        namespace (_type_): Pinecone 네임스페이스

    Returns:
        vector_store: 생성된 벡터스토어
    """
    if index_name in pc.list_indexes().names():
        print(f'Index {index_name} already exists. Loading embeddings...', end='')
        vector_store = PineconeVectorStore.from_documents(
        documents=chunks, embedding=OpenAIEmbeddings(), index_name=index_name, namespace=namespace)
        
        while not pc.describe_index(index_name).status['ready']:
            time.sleep(1)
        
        print('Done')
    else:
        print(f'Creating index {index_name} and embeddings ...', end = '')
        pc.create_index(name=index_name, dimension=1536, metric='cosine',  spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            ))
        
        while not pc.describe_index(index_name).status['ready']:
            time.sleep(1)
        # Add to vectorDB using LangChain 
        vector_store = PineconeVectorStore.from_documents(
        documents=chunks, embedding=OpenAIEmbeddings(), index_name=index_name, namespace=namespace)
        print('Done')   
    return vector_store
    
def generate_vectorstore(chunks):
    """

    Args:
        chunks (List): 생성된 chunk

    Returns:
        vector_store: 임베딩된 vector 전달
    """
    index_name='docsembeddeings'
    chunks = chunks
    namespace = "docs_documents"
    
    vector_store = load_or_create_embeddings_index(index_name=index_name, chunks=chunks, namespace=namespace)

    return vector_store