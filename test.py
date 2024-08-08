from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import OpenAIEmbeddings, OpenAI, ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import llm
import os
os.environ["OPENAI_API_KEY"] = "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"

def Article_Generator(content) :
    print(f"content: {content}")
    llm_chat = ChatOpenAI(model="gpt-4o-mini",max_tokens=6000,temperature=0)
    # Design the prompt
    prompt_chat = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(
                "你是一個很有質感的文章生成機器人，你接下來會依據使用著的要求幫使用著生成文章。"
            ),
            HumanMessagePromptTemplate.from_template("{content}")
        ]
    )
    # Initialize the LLMChain
    conversation_chat = llm.LLMChain(
        llm=llm_chat,
        prompt=prompt_chat,
        verbose=False,)
    response = conversation_chat({"content":content})
    return response

print(Article_Generator('幫我生成一個童話故事')['text'])