import os
from openai import OpenAI
from dotenv import load_dotenv
from google import genai
from google.genai import types
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage # 用於初始化 Agent

load_dotenv()
XAI_BASE_URL = "https://api.x.ai/v1"
gpt_client = OpenAI()
gemini_client = genai.Client()
grok_client = OpenAI(
        api_key=os.environ.get("XAI_API_KEY"),
        base_url=XAI_BASE_URL
    )


def gpt_web_search(prompt: str):
    """
    使用 OpenAI GPT 模型和其內建的 'web_search' 工具進行網路搜尋。

    Args:
        prompt: 使用者的查詢。
    """
    print(f"--- 使用 GPT 進行網路搜尋 (模型: gpt-5) ---")
    try:
        # 在 tools 參數中啟用 web_search 工具
        response = gpt_client.responses.create(
            model="gpt-5", # 選擇一個支援 web search 的模型
            tools=[
                {"type": "web_search"}
            ],
            input=prompt
        )

        # 檢查是否有搜尋呼叫被執行
        search_call = next((item for item in response.output if item.type == 'web_search_call'), None)
        
        if search_call:
            print(f"✅ 模型執行了網路搜尋。")
            # 這裡可以選擇性地顯示搜尋到的內容或摘要
            # 實際的搜尋結果會被模型用來生成 response.output_text
        else:
            print("ℹ️ 模型認為不需要網路搜尋，直接回答。")


        # 取得模型生成的文字回覆
        output_text = next((item for item in response.output if item.type == 'message'), None)
        
        if output_text:
            print(f"\n[GPT 回覆]\n{output_text.content[0].text}")
            
            # 顯示引用來源
            # annotations = next((item.annotations for item in response.output if item.type == 'message'), [])
            # if annotations:
            #     print("\n[引用來源]")
            #     for i, ann in enumerate(annotations):
            #         print(f"  {i+1}. 來源: {ann.text} (URL: {ann.url})")
        else:
            print("❌ 模型未產生文字回覆。")

    except Exception as e:
        print(f"\n發生錯誤: {e}")

def gemini_web_search(prompt: str):
    """
    使用 Google Gemini 模型和 'google_search' 工具進行網路搜尋。

    Args:
        prompt: 使用者的查詢。
    """
    print(f"--- 使用 Gemini 進行網路搜尋 (模型: gemini-2.5-flash) ---")
    try:
        # 在 tools 參數中啟用 google_search 工具
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[{"google_search": {}}]  # 啟用 Google Search Grounding
            )
        )

        print(f"\n[Gemini 回覆]\n{response.text}")

        # 檢查是否有搜尋元數據 (groundingMetadata)
        if response.candidates and response.candidates[0].grounding_metadata:
            metadata = response.candidates[0].grounding_metadata
            
            # 顯示模型實際使用的搜尋查詢
            if metadata.web_search_queries:
                print(f"✅ 模型執行的搜尋查詢: {', '.join(metadata.web_search_queries)}")
            
        else:
            print("ℹ️ 模型未執行網路搜尋或未提供引用來源。")

    except Exception as e:
        print(f"\n發生錯誤: {e}")
        print("請檢查 API 金鑰是否有效，或模型名稱是否正確。")

def grok_web_search(prompt: str):
    """
    使用 Grok 模型和其 Live Search 功能進行網路搜尋 (概念性範例)。
    
    注意: Grok 的 API 參數可能會隨著 xAI 的文件更新而改變。
    此範例使用與 Grok API 文件中常見的 OpenAI 兼容方式。

    Args:
        prompt: 使用者的查詢。
    """
    print(f"--- 使用 Grok 進行網路搜尋 (模型: grok-3) ---")
    try:
        # Grok 的 Live Search 通常是透過 `extra_body` 或類似的參數傳遞
        # 這裡假設它使用一個名為 `search_parameters` 的參數
        response = grok_client.chat.completions.create(
            model="grok-3", # 選擇一個 Grok 模型
            messages=[
                {"role": "user", "content": prompt}
            ],
            # 這是啟用 Live Search 的關鍵部分，具體名稱需參考 xAI 官方文件
            extra_body={
                "search_parameters": {
                    "mode": "auto" # "auto" 讓模型決定是否搜尋
                }
            }
        )

        # 取得模型生成的文字回覆
        reply = response.choices[0].message.content
        print(f"\n[Grok 回覆]\n{reply}")
        
        # Grok 的引用來源 (citations) 通常也會在 response 中
        # 由於我無法呼叫實際的 Grok API，這裡不提供 citation 處理的程式碼
        # 但通常可以在 `response.choices[0].message.tool_calls` 或其他欄位中找到

    except Exception as e:
        print(f"\n發生錯誤: {e}")
        print("請檢查 API 金鑰是否有效、base_url 是否正確，或 Grok API 參數是否已更新。")

def langchain_web_search_agent(prompt: str):
    print("--- 使用新的 LangChain Agent Executor 建立網路搜尋 Chain ---")
    try:
        # 1. 初始化 LLM 模型和工具
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        
        # 2. 定義 Agent Prompt
        # 必須包含 {tools}, {input}, {agent_scratchpad} 變數
        # prompt_template = ChatPromptTemplate.from_messages(
        #     [
        #         ("system", "你是一個樂於助人的 AI 助理。請務必使用提供的工具來回答關於最新資訊的問題。"),
        #         ("human", "{input}"),
        #         ("placeholder", "{agent_scratchpad}"), # Agent 思考和工具呼叫的紀錄
        #     ]
        # )

        # 3. 建立 Agent
        # create_tool_calling_agent 專門用於支持工具呼叫的模型 (如 GPT-4o-mini)
        agent = create_agent(model=llm, tools=None)

        # 4. 建立 Agent Executor (執行器)
        # agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        # 5. 執行 Agent Executor
        print(f"\n[Agent 思考與執行過程]")
        result = agent.invoke({"input": prompt})
        
        print(f"\n[LangChain Agent 最終回覆]\n{result['output']}")

    except Exception as e:
        print(f"\n發生錯誤: {e}")
        print("請檢查 API 金鑰是否有效，或套件是否已安裝。")

# 範例使用
langchain_web_search_agent("96分鐘什麼時候上映?請提供最新的資訊並引用來源。")
# grok_web_search("ImportError: cannot import name 'create_tool_calling_agent' from 'langchain.agents' 怎麼解決")
# gemini_web_search("96分鐘什麼時候上映?請提供最新的資訊並引用來源。")
# gpt_web_search("哪一隻MLB球隊對徐若熙感興趣?請提供最新的資訊並引用來源。")