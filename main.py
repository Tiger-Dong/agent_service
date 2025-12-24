import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置 OpenAI Client 连接到本地 Ollama
client = OpenAI(
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
    api_key=os.getenv("OLLAMA_API_KEY", "ollama")  # Ollama 不需要真实 API key，但 OpenAI 库要求提供
)

MODEL_NAME = os.getenv("MODEL_NAME", "qwen3:8b")

def ask_qwen(prompt: str) -> str:
    """
    使用 OpenAI Client 方式调用本地 Ollama 模型
    Args:
        prompt: 用户输入的问题
    Returns:
        模型的回答
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": prompt}
            ],
            stream=False,  # 非流式输出
            temperature=0.7,
            timeout=120
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"错误：{str(e)}"


if __name__ == "__main__":
    print(f"✅ 使用 OpenAI Client 连接本地 Ollama 模型: {MODEL_NAME}")
    print("输入 exit 或 quit 退出\n")

    while True:
        user_input = input("User：")
        if user_input.lower() in ("exit", "quit"):
            print("再见！")
            break

        if not user_input.strip():
            continue

        answer = ask_qwen(user_input)
        print(f"\nAssistant：{answer}\n")