from coreAgent.Agent import main_stream
import asyncio

print("金融客服智能体 - 输入'quit'退出")
print("=" * 50)

while True:
    context = input("User: ")  # 获取用户输入

    # 退出命令
    if context.lower() in ['quit', 'exit', '退出', 'q']:
        print("再见！")
        break

    # 跳过空输入
    if not context.strip():
        continue

    # 运行流式输出主函数
    asyncio.run(main_stream(context))
    print()  # 添加空行分隔
