import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()

"""链接云数据库"""
# chroma_client = chromadb.CloudClient(
#     database='product',
#     api_key=os.getenv('Chroma_API_KEY')
# )

"""自定义想量化数据库模型"""
class MyEmbeddingFunction(EmbeddingFunction):
    def __init__(self,api_key:str,model_name:str="text-embedding-v4",base_url:str="https://dashscope.aliyuncs.com/compatible-mode/v1"):
        self._client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        self._model_name=model_name
        
        
    def __call__(self, input: Documents) -> Embeddings:
        response = self._client.embeddings.create(
            model=self._model_name,
            input=input,
        )
        embeddings_list = [item.embedding for item in response.data]

        return embeddings_list # type: ignore

embeddings_api_key = os.getenv('DASHSCOPE_API_KEY')

if not embeddings_api_key:
    raise ValueError("Please set the DASHSCOPE_API_KEY environment variable.")

QwenEmbeddingModel = MyEmbeddingFunction(api_key=embeddings_api_key,model_name="text-embedding-v4")

"""本地持久化数据"""
client = chromadb.PersistentClient(path=r"D:\Qwen_AI\chromaData")

collection = client.get_or_create_collection(
    name="product",
    embedding_function=QwenEmbeddingModel,
    )

# 插入测试数据（已注释，使用 import_data.py 导入正式数据）
# collection.upsert(
#     ids=["id1", "id2"],
#     documents=[
#         "This is a document about pineapple",
#         "This is a document about oranges"
#     ]
# )
#
# results = collection.query(
#     query_texts=["pineapple"],
#     n_results=3
# )
# print(results)
