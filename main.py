import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3:8b"

def ask_qwen(prompt: str) -> str:
    payload = { # 像个字典，使用什么模型，传入什么提示词
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False # 不使用流式输出，一次性返回完整回答，不是一个一个字发，好处思考完整，坏处是等待时间较长。（TTFT 使用 First Token Time）
        #流式需更改调用用方式
    }

    response = requests.post(
        OLLAMA_URL, # 使用本地部署的 Qwen3:8b 模型，常量 OLLAMA_URL 指向本地服务器地址，定义模型名称 MODEL_NAME
        headers={"Content-Type": "application/json"}, # 设置请求头，使用 JSON 格式，（改成Open AI 的格式）
        data=json.dumps(payload), #
        timeout=120
    )

    response.raise_for_status()
    return response.json()["response"]


if __name__ == "__main__":
    print("✅ 本地 Qwen3:8b 已连接，输入 exit 退出\n")

    while True:
        user_input = input("User：")  # 获取用户输入，以后要通过其他方式替换
        if user_input.lower() in ("exit", "quit"):
            break

        answer = ask_qwen(user_input)
        print(f"\nQwen3：{answer}\n")