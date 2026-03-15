"""
测试 Agent 的多轮对话和记忆功能

运行方式: python -m test.test_agent_memory
"""
import sys
sys.path.insert(0, '.')

from agent.agent_core import create_shopping_agent, run_agent


if __name__ == '__main__':
    print("=" * 60)
    print("多轮对话测试 - 输入问题开始对话，输入 'quit' 退出")
    print("=" * 60)

    # 创建 agent 实例（整个测试过程复用同一个实例）
    agent = create_shopping_agent()

    while True:
        user_input = input("\n你: ").strip()

        if user_input.lower() in ['quit', 'exit', 'q', '退出']:
            print("再见！")
            break

        if not user_input:
            continue

        print("\nAgent 思考中...\n")
        result = run_agent(agent, user_input)

        print("=" * 60)
        print("Agent 回复:")
        print("-" * 60)
        print(result['output'])
        print("-" * 60)

        if result['steps']:
            print("\n调用工具:")
            for i, step in enumerate(result['steps'], 1):
                print(f"  {i}. {step['tool']}: {step['input']}")
