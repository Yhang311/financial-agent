"""
数据导入脚本
将金融知识库数据（产品信息、常见问答）导入到ChromaDB向量数据库
"""
import json
from pathlib import Path
from tools.chroma import collection

# Qwen embedding API批量限制
BATCH_SIZE = 10


def import_products():
    """导入银行贷款产品信息到向量数据库"""
    products_dir = Path("data/products")

    if not products_dir.exists():
        print(f"目录不存在: {products_dir}")
        return 0

    documents = []
    ids = []
    metadatas = []

    for file in products_dir.glob("*.json"):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # 构建文档内容：将所有信息整合成一个描述性文本
                doc_content = f"""
【产品名称】{data.get('name', '')}
【产品类别】{data.get('category', '')}
【产品描述】{data.get('description', '')}
【利率】{data.get('interest_rate', '')}
【最高额度】{data.get('max_amount', '')}
【最长期限】{data.get('max_term', '')}
                """.strip()

                documents.append(doc_content)
                ids.append(data.get('id', file.stem))
                metadatas.append({
                    "name": data.get('name', ''),
                    "category": data.get('category', ''),
                    "type": "product"
                })
                print(f"已读取产品: {data.get('name', '')}")

        except Exception as e:
            print(f"读取文件 {file} 失败: {e}")

    if documents:
        # 清空现有产品数据（可选）
        # collection.delete(where={"type": "product"})

        # 分批导入（每批最多BATCH_SIZE条）
        total_imported = 0
        for i in range(0, len(documents), BATCH_SIZE):
            batch_docs = documents[i:i+BATCH_SIZE]
            batch_ids = ids[i:i+BATCH_SIZE]
            batch_metas = metadatas[i:i+BATCH_SIZE]

            collection.upsert(
                documents=batch_docs,
                ids=batch_ids,
                metadatas=batch_metas
            )
            total_imported += len(batch_docs)
            print(f"已导入 {total_imported}/{len(documents)} 个产品")

        print(f"\n成功导入 {len(documents)} 个产品信息")
        return len(documents)
    else:
        print("没有找到产品数据")
        return 0


def import_qa():
    """导入常见问答到向量数据库，支持两种格式"""
    qa_dir = Path("data/qa")

    if not qa_dir.exists():
        print(f"目录不存在: {qa_dir}")
        return 0

    documents = []
    ids = []
    metadatas = []

    for file in qa_dir.glob("*.json"):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # 判断数据格式：嵌套格式还是单条问答格式
                if isinstance(data, dict):
                    # 检查是否为嵌套格式（如：{"工行-烟火贷": [{question, answer}, ...]}）
                    has_nested_qa = any(isinstance(v, list) for v in data.values())

                    if has_nested_qa:
                        # 嵌套格式：遍历每个产品类别
                        for category, qa_list in data.items():
                            if isinstance(qa_list, list):
                                for idx, qa in enumerate(qa_list):
                                    question = qa.get('question', '')
                                    answer = qa.get('answer', '')

                                    doc_content = f"""
【产品类别】{category}
【问题】{question}
【答案】{answer}
                                    """.strip()

                                    # 生成唯一ID
                                    unique_id = f"{file.stem}_{category}_{idx}"

                                    documents.append(doc_content)
                                    ids.append(unique_id)
                                    metadatas.append({
                                        "category": category,
                                        "question": question,
                                        "type": "qa"
                                    })
                                    print(f"已读取问答 [{category}]: {question[:40]}...")
                    else:
                        # 单条问答格式
                        doc_content = f"""
【问题】{data.get('question', '')}
【答案】{data.get('answer', '')}
【分类】{data.get('category', '')}
                        """.strip()

                        documents.append(doc_content)
                        ids.append(data.get('id', file.stem))
                        metadatas.append({
                            "question": data.get('question', ''),
                            "category": data.get('category', ''),
                            "type": "qa"
                        })
                        print(f"已读取问答: {data.get('question', '')}")

        except Exception as e:
            print(f"读取文件 {file} 失败: {e}")

    if documents:
        # 清空现有问答数据（可选）
        # collection.delete(where={"type": "qa"})

        # 分批导入（每批最多BATCH_SIZE条）
        total_imported = 0
        for i in range(0, len(documents), BATCH_SIZE):
            batch_docs = documents[i:i+BATCH_SIZE]
            batch_ids = ids[i:i+BATCH_SIZE]
            batch_metas = metadatas[i:i+BATCH_SIZE]

            collection.upsert(
                documents=batch_docs,
                ids=batch_ids,
                metadatas=batch_metas
            )
            total_imported += len(batch_docs)
            print(f"已导入 {total_imported}/{len(documents)} 个问答")

        print(f"\n成功导入 {len(documents)} 个问答")
        return len(documents)
    else:
        print("没有找到问答数据")
        return 0


def import_all():
    """导入所有数据"""
    print("=" * 50)
    print("开始导入金融知识库数据")
    print("=" * 50)

    print("\n[1/2] 导入产品信息...")
    product_count = import_products()

    print("\n[2/2] 导入常见问答...")
    qa_count = import_qa()

    print("\n" + "=" * 50)
    print(f"导入完成！产品: {product_count} 条, 问答: {qa_count} 条")
    print("=" * 50)

    # 验证导入
    count = collection.count()
    print(f"向量数据库中共有 {count} 条数据")


if __name__ == "__main__":
    import_all()
