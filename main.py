import os
from openai import OpenAI
from dotenv import load_dotenv
from geocoding import NominatimGeocoder

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


def show_menu():
    """显示主菜单"""
    print("\n" + "=" * 60)
    print("🎯 多功能智能助手")
    print("=" * 60)
    print("📋 可用模式：")
    print("  1️⃣  AI对话模式 - 与 Ollama AI 进行对话")
    print("  2️⃣  地图查询模式 - 查询地址的经纬度坐标")
    print("=" * 60)
    print("💡 提示：在任意模式中输入 '返回菜单' 可返回主菜单")
    print("       输入 'exit' 或 'quit' 可退出程序\n")


def ai_chat_mode():
    """AI 对话模式"""
    print("\n" + "=" * 60)
    print(f"🤖 AI对话模式已启动 - 模型: {MODEL_NAME}")
    print("=" * 60)
    print("💬 你可以开始与 AI 对话了！")
    print("📌 输入 '返回菜单' 返回主菜单\n")
    
    while True:
        user_input = input("User：").strip()
        
        if user_input.lower() in ("exit", "quit", "退出"):
            print("👋 再见！")
            return "exit"
        
        if user_input.lower() in ("返回菜单", "菜单", "menu", "back"):
            print("🔄 正在返回主菜单...\n")
            return "menu"
        
        if not user_input:
            continue
        
        answer = ask_qwen(user_input)
        print(f"\nAssistant：{answer}\n")


def map_query_mode():
    """地图查询模式"""
    print("\n" + "=" * 60)
    print("🌍 地图查询模式已启动 - OpenStreetMap 地理编码")
    print("=" * 60)
    print("📍 输入地址获取经纬度坐标")
    print("📌 输入 '返回菜单' 返回主菜单\n")
    
    geocoder = NominatimGeocoder()
    
    while True:
        address = input("请输入地址: ").strip()
        
        if address.lower() in ("exit", "quit", "退出"):
            print("👋 再见！")
            return "exit"
        
        if address.lower() in ("返回菜单", "菜单", "menu", "back"):
            print("🔄 正在返回主菜单...\n")
            return "menu"
        
        if not address:
            continue
        
        print(f"\n🔍 正在查询: {address}")
        result = geocoder.geocode(address)
        
        if result:
            print(f"\n✅ 查询成功！")
            print(f"📍 经度 (Longitude): {result['longitude']}")
            print(f"📍 纬度 (Latitude): {result['latitude']}")
            print(f"📝 完整地址: {result['display_name']}")
            print(f"⭐ 匹配度: {result['importance']:.2f}")
        else:
            print(f"\n❌ 未找到该地址，请尝试更具体的地址")
        
        print("\n" + "-" * 50 + "\n")


def main():
    """主程序入口"""
    while True:
        show_menu()
        
        choice = input("请选择模式（输入数字或模式名称）：").strip()
        
        if choice.lower() in ("exit", "quit", "退出"):
            print("👋 感谢使用，再见！")
            break
        
        result = None
        
        # 处理用户输入（转为小写进行匹配）
        choice_lower = choice.lower()
        if choice_lower in ("1", "ai对话模式", "ai对话", "ai", "对话模式", "对话"):
            result = ai_chat_mode()
        elif choice_lower in ("2", "地图查询模式", "地图查询", "地图模式", "地图", "查询模式", "查询"):
            result = map_query_mode()
        else:
            print("❌ 无效的选择，请重新输入\n")
            continue
        
        # 如果用户选择退出，则结束程序
        if result == "exit":
            print("👋 感谢使用，再见！")
            break


if __name__ == "__main__":
    main()