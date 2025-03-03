
from openai import Client
import os
from langchain_community.chat_models import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever
from langchain.chains import create_retrieval_chain
from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.documents import Document
from langchain import hub 
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_community.llms import Cohere

# re-rank Cohere key값 설정 
os.environ["COHERE_API_KEY"] = "input_your_key"
# OpenAI key값 설정 
os.environ["OPENAI_API_KEY"] = "input_your_key"
openai = Client()


# Retrieval Chain 생성

class Query_Answer:
      def __init__(self):
            pass


def create_history_aware_retriever_with_hub(vector_store, question, chat_history=[]):

   
    
    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")

    llm = ChatOpenAI(temperature=1)
    
    # retriever the search type(re-rank반영 mmr로 선택) 및 retriever 설정 
    retriever = vector_store.as_retriever(search_type='mmr', search_kwargs={'k':1,'fetch_k':10},include_metadata=True, metadata_key = 'source')
    # re-rank retriever 설정 
    llm_cohere = Cohere(temperature=0)
    compressor = CohereRerank(model="rerank-english-v3.0")
    compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=retriever)


    # 첫번째 Chain    
    chat_retriever_chain = create_history_aware_retriever(
        llm_cohere, compression_retriever, rephrase_prompt
    )
    
    qa_system_prompt = """You are an assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, just find. \
    Use three sentences maximum and keep the answer concise.\
    
    

    {context}"""

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    # 두번째 Chain
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    
    # Chain 결합
    rag_chain = create_retrieval_chain(chat_retriever_chain, question_answer_chain)
 

    result = rag_chain.invoke({"input": question, "chat_history": chat_history },return_source_documents=True)
    
    docs_and_scores = vector_store.similarity_search_with_score(question, k=1)
    agent = ""
    score = 0
    for doc, score in docs_and_scores:
            doc.metadata = {**doc.metadata, **{"score": score}}
            #print(doc.metadata)
            #print(score)

    if score < 0.80:
          agent = "General Agent"
          reference = 'None'
    else:
          if doc.metadata['source'] == "data/pdf_file1.pdf":
                agent = "DeepSeek Agent"
                reference = doc.metadata['source']
          elif doc.metadata['source'] == "data/ppt_file1.pptx":
                agent = "Rule Agent"
                reference = doc.metadata['source']
    
    
    
    # Append to Chat History 
    chat_history.append((question, result['answer']))
    
    return result, chat_history, agent, score, reference