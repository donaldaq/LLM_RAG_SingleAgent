import tiktoken


# 데이터 비용계산 함수 
class Calc_Cost:
    def __init__(self):
        pass
def calculate_and_display_embedding_cost(texts):
    """

    Args:
        texts (): 생성된 데이터 
    """
    enccoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    total_tokens = sum([len(enccoding.encode(page.page_content)) for page in texts])
    print(f'Total Tokens: {total_tokens}')
    print(f'Embedding Cost in USD:{total_tokens / 1000 * 0.0004:.6f}')

