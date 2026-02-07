"""
向量检索工具
将ChromaDB检索功能封装为LangChain Tool，供Agent使用
"""
from langchain_core.tools import tool
from tools.chroma import collection


@tool
def search_knowledge_base(query: str, n_results: int = 3) -> str:
    """
    查询本地金融知识库，获取银行贷款产品信息和常见问答。

    使用时机：
    - 用户询问贷款产品（个人贷款、企业贷款、房贷）
    - 用户询问贷款申请流程、利率计算、还款方式等
    - 用户询问已知产品信息或固定流程的问题

    不适用于：
    - 实时信息（如最新新闻、今日利率）→ 请使用webSearch工具
    - 当前市场数据（如今日股价、最新政策）→ 请使用webSearch工具

    参数:
        query: 搜索查询文本，例如"个人贷款利率"、"如何申请企业贷款"
        n_results: 返回结果数量，默认为3条

    返回:
        检索到的相关文档内容，按相似度排序
        如果未找到相关信息，建议使用webSearch联网搜索
    """
    try:
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )

        # 检查是否有结果
        if results['documents'] and results['documents'][0]:
            # 格式化输出结果
            output = []
            for i, doc in enumerate(results['documents'][0], 1):
                output.append(f"[相关文档 {i}]\n{doc}")
            return "\n\n".join(output)
        return "未找到相关信息，请尝试使用联网搜索获取最新信息。"

    except Exception as e:
        return f"知识库检索出错: {str(e)}"


if __name__ == "__main__":
    # 测试向量检索工具
    test_queries = [
        "个人贷款利率",
        "企业贷款申请条件",
        "房贷计算方式"
    ]

    for query in test_queries:
        print(f"\n查询: {query}")
        print("-" * 50)
        result = search_knowledge_base.invoke({"query": query, "n_results": 2})
        print(result)
