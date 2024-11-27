from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
from langchain.agents import load_tools
import pandas as pd
import os

# .env 파일 로드
def create_agent(df1, df2):
    load_dotenv()

# 환경 변수 가져오기
    google_api_key = os.getenv("GOOGLE_API_KEY")
    os.environ["GOOGLE_API_KEY"] = google_api_key

    llm= ChatGoogleGenerativeAI(temperature=0, model="gemini-1.5-pro-latest")

    serpapi_api_key = os.getenv("SERPAPI_API_KEY")
    os.environ["SERPAPI_API_KEY"] = serpapi_api_key
    tool_names = ['serpapi']
    tools = load_tools(tool_names)

    agent = create_pandas_dataframe_agent(
        llm,
        [df1, df2],
        verbose=True,
        allow_dangerous_code=True,
        extra_tools=tools,
        prefix="너는 서울 여행 정보 제공 역할 가이드야."
        "사용자가 물어보는 정보에 맞춰서 식당이나 관광지를 추천해주고 데이터프레임에 없는 정보는 직접 검색해서 알려줘"
        "일정을 짜달라고 하면 표 형식으로 최적의 일정을 나타내줘"
        "모든 답변은 한국어로 해"
    )
        
    return agent



if __name__ == "__main__":

    seoul_food = pd.read_csv('C:/Users/park2/OneDrive/바탕 화면/NIPA/seoul_food/seoul_food.csv')
    seoul_place = pd.read_csv('C:/Users/park2/OneDrive/바탕 화면/NIPA/seoul_place/seoul_place.csv')

    agent = create_agent(df1=seoul_food, df2=seoul_place)

    question = '종로 커플 데이트 장소 알려주라'
    result= agent.invoke(question)
    print(result['output'])