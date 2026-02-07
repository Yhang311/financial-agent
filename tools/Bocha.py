import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()


def Bocha() -> Dict[str, Any]:
    """
    创建博查AI MCP服务器配置

    Returns:
        MCP服务器连接配置字典

    Raises:
        ValueError: 当BOCHA_API_KEY环境变量未设置时
    """
    api_key = os.getenv('BOCHA_API_KEY')
    if not api_key:
        raise ValueError("请设置BOCHA_API_KEY环境变量")

    return {
        "url": "https://mcp.bochaai.com/sse",
        "transport": "sse",
        "headers": {
            "Authorization": f"Bearer {api_key}"
        }
    }


if __name__ == "__main__":
    bocha = Bocha()
    print(bocha)
