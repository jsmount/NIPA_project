from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma


# ================================================================
# # CSV 로더 생성
# loader = CSVLoader(file_path="C:/Users/park2/OneDrive/바탕 화면/NIPA/seoul_food/seoul_food.csv", 
#                    encoding='utf-8',
#                    csv_args={
#                         "delimiter": ",",  # 구분자
#                         "quotechar": '"',  # 인용 부호 문자
#                         "fieldnames": [
#                             'name',
#                             'category',
#                             'rating',
#                             'address'
#         ],  # 필드 이름
#     },)

# # 데이터 로드
# docs = loader.load()
# ===================================================================



# =======================================================================
# # page_content 데이터만 추출
# page_contents = [doc.page_content for doc in docs]

# # txt 파일로 저장
# # page_content만 추출하여 txt 파일로 저장
# output_file = "seoul_food_page_contents.txt"

# # 파일 생성 및 저장
# with open(output_file, 'w', encoding='utf-8') as f:
#     for doc in docs:
#         # Document 객체의 page_content 속성에 접근
#         f.write(doc.page_content + '\n\n')  # 각 page_content를 두 줄 띄워 구분

# print(f"{output_file} 파일이 생성되었습니다.")
# ==========================================================================



# 파일 읽기 시 인코딩 설정
# with open("./seoul_food_page_contents.txt", "r", encoding="utf-8") as f:  # utf-8로 파일 읽기
#     file = f.read()  # 파일 내용을 읽어옵니다.

text_splitter = RecursiveCharacterTextSplitter(
    # 청크 크기를 매우 작게 설정합니다. 예시를 위한 설정입니다.
    chunk_size=250,
    # 청크 간의 중복되는 문자 수를 설정합니다.
    chunk_overlap=25,
    # 문자열 길이를 계산하는 함수를 지정합니다.
    length_function=len,
    # 구분자로 정규식을 사용할지 여부를 설정합니다.
    is_separator_regex=False,
)

# # text_splitter를 사용하여 file 텍스트를 문서로 분할합니다.
# texts = text_splitter.create_documents([file])
# print(texts[0])  # 분할된 문서의 첫 번째 문서를 출력합니다.
# print("===" * 20)
# print(texts[1])  # 분할된 문서의 두 번째 문서를 출력합니다.

loader1 = TextLoader('C:/Users/park2/OneDrive/바탕 화면/NIPA/langchain/seoul_food_page_contents.txt')

split_doc1 = loader1.load_and_split(text_splitter)
print(len(split_doc1))