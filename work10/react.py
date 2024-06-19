import os
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain.agents import load_tools
from langchain.agents import initialize_agent

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中获取 Serper 和 Groq 的 API 密钥
serper_api_key = os.getenv("SERPER_API_KEY")
groq_api_key = os.getenv("ChatGroq_API_KEY")

# 设置 API 密鑰環境變量
os.environ["SERPER_API_KEY"] = 'de0aca21fe5858e028eb0d7b2430f4e76fd385bf'
os.environ["ChatGroq_API_KEY"] = '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'#chatgroq

# 初始化 Groq 模型
llm = ChatGroq(api_key=groq_api_key)

# 加载工具
tools = load_tools(["google-serper", "llm-math"], llm=llm)

# 初始化代理
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# 执行查询
try:
    result = agent.run("奥利维亚·王尔德的男朋友是谁?他现在的年龄的0.23次方是多少?用中文回答")
    print(result)
except Exception as e:
    print(f"Error: {e}")

