"""
智能代理主程序
此程序创建一个AI代理，能够接收用户输入，使用工具并返回答案。
"""
import sys
from pathlib import Path
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
import asyncio

# 添加模型目录到路径，以便导入qwen_plus模型
from model.models import qwen_plus, qwen_max, qwen_image_max
# 添加工具目录到路径，以便导入Bocha工具
from tools.Bocha import Bocha
# 添加向量检索工具
from tools.vector_retriever import search_knowledge_base


system_prompt = """
你是一个专业的金融客服助手。你拥有以下工具来帮助用户：

1. **search_knowledge_base** - 查询本地金融知识库（贷款产品、常见问答）
2. **webSearch** - 联网搜索最新实时信息

## 工作流程（必须严格遵守）：

### 第一步：判断问题类型
- 如果问题关于贷款产品（个人贷款、企业贷款、房贷）或常见金融问题 → 使用 search_knowledge_base
- 如果问题涉及实时信息（今日新闻、最新利率、当前政策）→ 使用 webSearch
- 如果不确定 → 先使用 search_knowledge_base，如果没有相关信息再使用 webSearch

### 第二步：直接调用工具
- **直接执行工具调用，不要询问用户偏好**
- **不要说"我可以搜索"、"让我为您查找"等话术**
- **直接调用工具，然后基于工具返回的结果回答**

### 第三步：基于工具结果回答
- 使用工具返回的信息来回答用户
- 保持专业、友好的服务态度
- 不提供投资建议或承诺收益

## 示例：
- 用户问"今天的金融新闻" → 直接调用 webSearch("今日最新金融新闻")
- 用户问"个人贷款利率" → 直接调用 search_knowledge_base("个人贷款利率")
- 用户问"最新LPR利率" → 直接调用 webSearch("最新LPR利率报价")

## 重要提醒：
- **必须调用工具，不要只凭知识回答**
- **不要说"我可以帮你搜索"，直接去搜索**
- **工具调用是自动的，不需要用户确认**
"""


async def Agent():
    """
    初始化MCP客户端并获取可用工具
    返回从客户端获取的工具列表与本地工具的合并列表
    """
    # 加载MCP工具（联网搜索）
    client = MultiServerMCPClient({
        "webSearch": Bocha()  # 使用Bocha工具进行网络搜索
    })
    mcp_tools = await client.get_tools()

    # 加载本地向量检索工具
    local_tools = [search_knowledge_base]

    # 合并所有工具
    tools = mcp_tools + local_tools
    return tools



async def main(context):
    """
    主函数 - 创建并运行AI代理（非流式）
    参数 context: 用户输入的上下文
    """
    # 加载大语言模型
    llm = qwen_plus()

    # 获取可用工具
    tools = await Agent()

    # 使用LLM、工具和系统提示词创建智能代理
    agent = create_agent(llm, tools, system_prompt=system_prompt)

    # 异步调用代理处理用户消息
    response = await agent.ainvoke({"messages": context})

    # 解析并输出AI的回复
    # 检查响应是否为包含消息的字典
    if isinstance(response, dict) and 'messages' in response:
        messages = response['messages']  # 获取消息列表

        # 收集所有AI消息（最终答案通常是最后一个AI消息）
        ai_messages = []
        for msg in messages:
            if hasattr(msg, 'type') and msg.type == 'ai':
                ai_messages.append(msg)

        # 打印最后一个AI消息（最终答案）
        if ai_messages:
            final_msg = ai_messages[-1]
            if hasattr(final_msg, 'content'):
                print(f"AI: {final_msg.content}")
            else:
                print(f"AI: {final_msg}")
        else:
            # 没有AI消息，打印调试信息
            print("调试: 消息列表内容:")
            for i, msg in enumerate(messages):
                print(f"  [{i}] type: {getattr(msg, 'type', 'unknown')}, content: {str(msg)[:100]}")
    else:
        print(f"响应: {response}")  # 如果响应不是预期格式，直接打印


async def main_stream(context):
    """
    流式输出版本 - 使用ainvoke获取响应（临时回退方案）
    参数 context: 用户输入的上下文
    """
    # 加载大语言模型
    llm = qwen_plus()

    # 获取可用工具
    tools = await Agent()

    # 使用LLM、工具和系统提示词创建智能代理
    agent = create_agent(llm, tools, system_prompt=system_prompt)

    # 先显示思考状态
    print("AI: 思考中...", end="", flush=True)

    # 使用非流式调用获取完整响应
    response = await agent.ainvoke({"messages": context})

    # 清除思考状态
    print("\r    \r", end="", flush=True)
    print("AI: ", end="", flush=True)

    # 解析并输出AI的回复
    if isinstance(response, dict) and 'messages' in response:
        messages = response['messages']
        ai_messages = [msg for msg in messages if hasattr(msg, 'type') and msg.type == 'ai']
        if ai_messages:
            final_msg = ai_messages[-1]
            content = getattr(final_msg, 'content', None)
            if content:
                print(content, end="", flush=True)

    print()  # 输出完成后换行

if __name__ == '__main__':
    """
    程序入口点
    获取用户输入并启动AI代理处理流程
    """
   # context = input("User: ")  # 获取用户输入
    #asyncio.run(main(context))  # 运行异步主函数
