import os
from openai import OpenAI
from dotenv import load_dotenv
from google import genai
from google.genai import types
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_core.tools import Tool
from langchain_community.utilities import SearchApiAPIWrapper
from langchain_xai import ChatXAI
from langchain_google_genai import ChatGoogleGenerativeAI




load_dotenv()
search = SearchApiAPIWrapper()
XAI_BASE_URL = "https://api.x.ai/v1"
gpt_client = OpenAI()
gemini_client = genai.Client()
grok_client = OpenAI(
        api_key=os.environ.get("XAI_API_KEY"),
        base_url=XAI_BASE_URL
    )
web_tool = Tool(
    name="web_search",
    func=search.run,
    description="在網路上搜尋最新資訊"
)

def gpt_web_search(prompt: str):
    try:
        response = gpt_client.responses.create(model="gpt-5",tools=[{"type": "web_search"}],input=prompt) 
        output_text = next((item for item in response.output if item.type == 'message'), None)
        print(f"\n[GPT 回覆]\n{output_text.content[0].text}")
    except Exception as e:
        print(f"\n發生錯誤: {e}")

def gemini_web_search(prompt: str):
    try:
        response = gemini_client.models.generate_content(model='gemini-2.5-flash',contents=prompt,config=types.GenerateContentConfig(tools=[{"google_search": {}}]))
        print(f"\n[Gemini 回覆]\n{response.text}")
    except Exception as e:
        print(f"\n發生錯誤: {e}")

def grok_web_search(prompt: str):
    try:
        response = grok_client.chat.completions.create(model="grok-3",messages=[{"role": "user", "content": prompt}],extra_body={"search_parameters": {"mode": "auto"}}      )
        reply = response.choices[0].message.content
        print(f"\n[Grok 回覆]\n{reply}")
    except Exception as e:
        print(f"\n發生錯誤: {e}")

# ===========================
# 定義 web.run 工具
# ===========================

def langchain_web_search_agent(user_message: str):
    print("--- 使用新的 LangChain Agent Executor 建立網路搜尋 Chain ---")
    try:
        # 1. 初始化 LLM 模型和工具
        # llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        llm = ChatXAI(model_name="grok-3", api_key=os.getenv("XAI_API_KEY"))
        # llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, convert_system_message_to_human=True)
        
        # 2. 定義系統提示語
        system_message = (
            "你是一個樂於助人的 AI 助理。"
            "當用戶提到任何需要最新資訊的內容時，務必使用 web_search 工具執行搜尋。"
            "請在回答中引用你所使用的來源。"
            "如果用戶的問題不需要最新資訊，則直接回答即可。"
            "請確保回答簡潔且有條理。"
            "記住，只在必要時使用 web_search 工具。"
        )

        # 3. 建立 Agent
        # create_tool_calling_agent 專門用於支持工具呼叫的模型 (如 GPT-4o-mini)
        agent = create_agent(model=llm, tools=[web_tool],system_prompt=system_message)

        # 4. 建立 Agent Executor (執行器)
        # agent_executor = AgentExecutor(agent=agent, tools=[web_tool], verbose=True)

        # 5. 執行 Agent Executor
        print(f"\n[Agent 思考與執行過程]")
        result = agent.invoke({
            "messages": [
                HumanMessage(content=user_message)
            ]
        })
        
        print(f"\n[LangChain Agent 最終回覆]\n{result['messages']}")

    except Exception as e:
        print(f"\n發生錯誤: {e}")
        print("請檢查 API 金鑰是否有效，或套件是否已安裝。")

# 範例使用
langchain_web_search_agent("幫我查詢台幣對日幣的匯率是多少，並引用來源。")
langchain_web_search_agent("100 公里等於多少英里？")
# grok_web_search("ImportError: cannot import name 'create_tool_calling_agent' from 'langchain.agents' 怎麼解決")
# gemini_web_search("96分鐘什麼時候上映?請提供最新的資訊並引用來源。")
# gpt_web_search("哪一隻MLB球隊對徐若熙感興趣?請提供最新的資訊並引用來源。")