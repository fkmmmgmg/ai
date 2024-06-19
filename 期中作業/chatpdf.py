import os
from langchain_groq import ChatGroq
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
import requests
from sentence_transformers import SentenceTransformer
from langchain.schema import Document
from langchain_community.vectorstores.utils import filter_complex_metadata

# 设置 API 密钥
os.environ["SERPER_API_KEY"] = 'de0aca21fe5858e028eb0d7b2430f4e76fd385bf'
os.environ["GROQ_API_KEY"] = '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'

def translate_to_traditional_chinese(text):
    url = "https://api.serper.dev/translate"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['SERPER_API_KEY']}"
    }
    payload = {
        "q": text,
        "target": "zh-TW"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'translatedText' in data:
            return data['translatedText']
        else:
            print("Error: 'translatedText' not found in the response.")
            print("Response JSON:", data)
            return text
    else:
        print("Error: Translation API request failed with status code", response.status_code)
        return text

file_path = "D:\\我的\\金門景觀\\Sensitivity of correlation structure of class- and landscape-levelmetrics in three diverse regionsliu2016.pdf"
loader = PyPDFLoader(file_path)
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
documents = loader.load_and_split(splitter)

# 打印 documents 的内容(檢查)
print("Documents loaded and split:")
for i, doc in enumerate(documents[:5]):  # 僅打印前 5 個文檔
    print(f"Document {i+1}: {doc.page_content[:100]}...")  # 僅打印前 100 個字符

# 提取文本内容
texts = [doc.page_content for doc in documents]

# 使用 SentenceTransformers 生成嵌入
embedder = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = embedder.encode(texts)

# 創建向量儲存
documents_with_embeddings = [
    Document(page_content=text, metadata={"embedding": embedding.tolist()})
    for text, embedding in zip(texts, embeddings)
]

# 打印部分 documents_with_embeddings 的内容(檢查)
print("Documents with embeddings:")
for i, doc in enumerate(documents_with_embeddings[:5]):  # 僅打印前 5 個
    print(f"Document {i+1}: {doc.page_content[:100]}...")  # 僅打印前 100 個字符

filtered_documents = []
for idx, doc in enumerate(documents_with_embeddings):
    if idx < 5:  # 僅打印前 5 個文檔的過濾前後信息(檢查)
        print(f"Processing Document {idx+1}")
        print(f"Before filtering - Type: {type(doc)}, Metadata: {doc.metadata}")
    filtered_doc = filter_complex_metadata([doc])[0]  # 注意這裡傳遞的是單元元素列表
    if idx < 5:  # 僅打印前 5 個文檔的過濾前後信息
        print(f"After filtering - Type: {type(filtered_doc)}, Metadata: {getattr(filtered_doc, 'metadata', 'No metadata')}")
    if not isinstance(filtered_doc, Document):
        filtered_doc = Document(page_content=filtered_doc.page_content, metadata=filtered_doc.metadata)
    filtered_documents.append(filtered_doc)

# 打印部分 filtered_documents 的内容(檢查)
print("Filtered documents:")
for i, doc in enumerate(filtered_documents[:5]):  # 僅打印前 5 個文檔
    print(f"Document {i+1}: {doc.page_content[:100]}...")  # 僅打印前 100 個字符

# 定義嵌入函数
class EmbeddingFunctionWrapper:
    def __init__(self, model):
        self.model = model

    def embed_documents(self, texts):
        return self.model.encode(texts).tolist()

    def embed_query(self, text):
        return self.model.encode([text]).tolist()[0]

embedding_function = EmbeddingFunctionWrapper(embedder)

# 創建 Chroma 向量儲存，並傳遞嵌入函数
vectorstore = Chroma.from_documents(documents=filtered_documents, embedding=embedding_function)

# 初始化 ChatGroq 模型
groq_api_key = os.environ["GROQ_API_KEY"]
groq_model = ChatGroq(groq_api_key=groq_api_key)

# 使用 ChatGroq 模型創建對話檢索
qa = ConversationalRetrievalChain.from_llm(groq_model, retriever=vectorstore.as_retriever())
chat_history = []

while True:
    query = input('\nQ: ')
    if not query:
        break
    translated_query = translate_to_traditional_chinese(query)
    result = qa({"question": translated_query, "chat_history": chat_history})
    translated_answer = translate_to_traditional_chinese(result['answer'])
    print('A:', translated_answer)
    chat_history.append((query, translated_answer))
