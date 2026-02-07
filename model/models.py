
from langchain_community.chat_models.tongyi import ChatTongyi
from dotenv import load_dotenv
from typing import Any  # noqa: F401
import os

load_dotenv()


"""
模型定义:
    定义qwen-plus和qwen-max模型
"""

class QwenModelFactory:
    """
    Qwen模型工厂类，提供创建不同Qwen模型的静态方法
    """


    @staticmethod
    def qwen_plus() -> Any:
        config = {
            "model_name": "qwen-plus",
            "temperature": 0.7,
            "max_tokens": 2048,
            "streaming": False,
            "api_key": os.getenv('DASHSCOPE_API_KEY'),
        }
        return ChatTongyi(**config)

    @staticmethod
    def qwen_max() -> Any:
        config = {
            "model_name": "qwen-max",
            "temperature": 0.7,
            "max_tokens": 2048,
            "api_key": os.getenv('DASHSCOPE_API_KEY'),
        }
        return ChatTongyi(**config)

    @staticmethod
    def qwen_image_max() -> Any:
        config = {
            "model_name": "qwen-image-max",
            "temperature": 0.7,
            "max_tokens": 2048,
            "api_key": os.getenv('DASHSCOPE_API_KEY'),
        }
        return ChatTongyi(**config)


qwen_plus = QwenModelFactory.qwen_plus
qwen_max = QwenModelFactory.qwen_max
qwen_image_max = QwenModelFactory.qwen_image_max


if __name__ == '__main__':
    """
    测试模型
    """
