# 金融客服智能体

基于 LangChain 和 Qwen 大模型开发的金融客服智能助手，支持知识库问答和联网搜索功能。

## 功能特性

- 🏦 **贷款产品咨询** - 支持个人贷款、企业贷款、房贷等产品信息查询
- 🔍 **常见问答** - 解答贷款申请流程、利率计算、还款方式等问题
- 🌐 **联网搜索** - 集成 Bocha AI 联网搜索，获取最新实时信息
- 📚 **向量知识库** - 基于 ChromaDB + Qwen Embedding 的本地知识库
- 🤖 **工具调用** - 使用 LangChain Agent 自动调用工具回答问题

## 技术栈

- **框架**: LangChain
- **大模型**: 通义千问 (Qwen Plus/Max)
- **向量数据库**: ChromaDB
- **嵌入模型**: Qwen text-embedding-v4
- **联网搜索**: Bocha AI (MCP协议)

## 项目结构

```
agentModel/
├── main.py                 # 主程序入口
├── coreAgent/
│   └── Agent.py           # Agent 核心逻辑
├── model/
│   └── models.py          # Qwen 模型定义
├── tools/
│   ├── chroma.py          # ChromaDB 向量数据库
│   ├── vector_retriever.py # 向量检索工具
│   ├── Bocha.py           # 联网搜索工具 (MCP)
│   ├── import_data.py     # 数据导入脚本
│   └── qdrant.py          # Qdrant 数据库 (备用)
├── data/
│   ├── products/          # 贷款产品数据
│   └── qa/                # 常见问答数据
├── requirements.txt        # Python 依赖
└── .env                   # 环境变量配置
```

## 安装

### 1. 克隆项目

```bash
git clone https://github.com/Yhang311/financial-agent.git
cd financial-agent
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

创建 `.env` 文件并填入 API 密钥：

```bash
DASHSCOPE_API_KEY=your_dashscope_api_key
BOCHA_API_KEY=your_bocha_api_key
```

## 使用方法

### 导入知识库数据

```bash
python -m tools.import_data
```

### 运行智能体

```bash
python main.py
```

### 示例对话

```
User: 工行烟火贷的要求是什么？
AI: 🔍 查询知识库... ✓
AI: 根据知识库查询，工行烟火贷的要求如下：借款人年龄18-65岁...

User: 今天的金融新闻
AI: 🔍 联网搜索... ✓
AI: 今天的金融新闻...
```

## 退出程序

输入 `quit`、`exit`、`退出` 或 `q` 退出程序。

## 开发说明

### 添加知识库数据

1. **产品数据** - 放入 `data/products/` 目录，JSON 格式：

```json
{
  "id": "prod_001",
  "name": "个人信用贷款",
  "category": "个人贷款",
  "description": "产品描述...",
  "interest_rate": "年化利率4.35%-8.5%",
  "max_amount": "50万元",
  "max_term": "5年"
}
```

2. **问答数据** - 放入 `data/qa/` 目录，JSON 格式：

```json
{
  "工行-烟火贷": [
    {
      "question": "借款人需要满足哪些条件？",
      "answer": "借款人年龄18-65岁..."
    }
  ]
}
```

### 模型配置

在 `model/models.py` 中修改模型参数：

```python
config = {
    "model_name": "qwen-plus",  # 或 qwen-max
    "temperature": 0.7,
    "max_tokens": 2048,
}
```

## 注意事项

- ⚠️ `.env` 文件包含敏感信息，不要提交到 Git
- ⚠️ 向量数据库路径 `D:\Qwen_AI\chromaData` 是绝对路径，请根据实际情况修改
- ⚠️ 联网搜索功能依赖外部 API，连接超时会自动降级到本地知识库

## 待优化功能

- [ ] 实现真正的流式输出（逐字显示）
- [ ] 添加对话历史记忆
- [ ] 优化工具调用状态显示
- [ ] 添加更多知识库数据
- [ ] 支持多轮对话上下文

## 许可证

MIT License

## 联系方式

GitHub: [@Yhang311](https://github.com/Yhang311)
