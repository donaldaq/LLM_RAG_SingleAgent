import os
from Docs_Loader import check_and_load_pdf_from_dir
from Chunks import generate_chunk
from Calc_Cost import calculate_and_display_embedding_cost
from Generate_VectorStore import generate_vectorstore
from Query_Answer import create_history_aware_retriever_with_hub
# 다양한 키값 설정 

os.environ["OPENAI_API_KEY"] = "input_your_key"
os.environ["PINECONE_API_KEY"] = "input_your_key"
os.environ['LANGCHAIN_API_KEY'] = "input_your_key"
os.environ['LANGCHAIN_PROJECT'] = "input_your_key"



if __name__ == "__main__":

    #1. File path 입력으로 문서 데이터 추출
    total_documents = check_and_load_pdf_from_dir('data')

    #2. Chunks 생성 
    chunks = generate_chunk(total_documents)

    #3. Chunk 비용확인
    calculate_and_display_embedding_cost(chunks)


    #2. Generation Vectorstore
    vector_store = generate_vectorstore(chunks)

    #3. Query and Answer
    chat_history = []
    question = "DeepSeek의 강화학습 기반 훈련 방식이 기존 LLM 훈련 방식 대비 AI 모델의 추론능력과 효율성에 미치는 영향은 무엇인가요?"
    #question = "남녀고용평등법상 직장 내 성희롱 행위자의 해당하는 범위에 대해 알려주세요."
    #question = "사랑이란 뭘까?"
    result, chat_history, agent, score, reference = create_history_aware_retriever_with_hub(vector_store, question, chat_history)

    print("사용자 질문: "+ question)
    print(agent +": "+ result['answer'])
    print("Chat History: ")
    print(chat_history)
    print("Similarity Score: " + str(score))
    print("Reference: " +reference)

