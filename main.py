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

# 全局设置
SETTINGS = {
    "language": "中文",  # 可选: "中文", "English"
    "show_thinking": False  # 是否显示 AI thinking 过程
}

# 模式匹配关键词
MODE_KEYWORDS = {
    "ai": ("1", "ai对话模式", "ai对话", "ai", "对话模式", "对话", "ai chat", "chat"),
    "map": ("2", "地图查询模式", "地图查询", "地图模式", "地图", "查询模式", "查询", "map", "query"),
    "settings": ("3", "设置", "settings", "配置", "setting")
}

# 多语言文本字典
TEXTS = {
    "中文": {
        "goodbye": "👋 再见！",
        "returning_menu": "🔄 正在返回主菜单...\n",
        "main_title": "🎯 多功能智能助手",
        "available_modes": "📋 可用模式：",
        "mode_ai": "  1️⃣  AI对话模式 - 与 Ollama AI 进行对话",
        "mode_map": "  2️⃣  地图查询模式 - 查询地址的经纬度坐标",
        "mode_settings": "  3️⃣  设置 - 配置语言和显示选项",
        "tip_return": "💡 提示：在任意模式中输入 '返回菜单' 可返回主菜单",
        "tip_exit": "       输入 'exit' 或 'quit' 可退出程序\n",
        "choose_mode": "请选择模式（输入数字或模式名称）：",
        "invalid_choice": "❌ 无效的选择，请重新输入\n",
        "thank_you": "👋 感谢使用，再见！",
        "ai_mode_title": "🤖 AI对话模式已启动 - 模型: {model}",
        "ai_mode_subtitle": "💬 你可以开始与 AI 对话了！",
        "return_menu_tip": "📌 输入 '返回菜单' 返回主菜单\n",
        "user_prompt": "User：",
        "assistant_prompt": "\nAssistant：{answer}\n",
        "ai_thinking": "\n🤔 AI 正在思考...\n",
        "map_mode_title": "🌍 地图查询模式已启动 - OpenStreetMap 地理编码",
        "map_mode_subtitle": "📍 输入地址获取经纬度坐标",
        "enter_address": "请输入地址: ",
        "searching": "\n🔍 正在查询: {address}",
        "query_success": "\n✅ 查询成功！",
        "longitude": "📍 经度 (Longitude): {lon}",
        "latitude": "📍 纬度 (Latitude): {lat}",
        "full_address": "📝 完整地址: {addr}",
        "importance": "⭐ 匹配度: {imp:.2f}",
        "address_not_found": "\n❌ 未找到该地址，请尝试更具体的地址",
        "settings_title": "⚙️  设置 / Settings",
        "current_settings": "📋 当前设置：",
        "setting_language": "  1️⃣  语言 / Language: {lang}",
        "setting_thinking": "  2️⃣  显示 AI Thinking: {status}",
        "modify_tip": "💡 输入数字修改设置，输入 '返回菜单' 返回\n",
        "choose_setting": "请选择要修改的设置：",
        "language_settings": "\n📝 语言设置 / Language Settings",
        "lang_option_cn": "  1. 中文",
        "lang_option_en": "  2. English",
        "select_language": "\n请选择语言 / Select language (1/2): ",
        "switched_to_cn": "✅ 已切换到中文",
        "switched_to_en": "✅ Switched to English",
        "invalid_lang_choice": "❌ 无效选择 / Invalid choice",
        "thinking_settings": "\n📝 AI Thinking 显示设置",
        "current_status": "  当前状态: {status}",
        "enable_thinking": "\n是否开启显示 AI thinking 过程？(y/n): ",
        "thinking_enabled": "✅ 已开启 AI thinking 显示",
        "thinking_disabled": "✅ 已关闭 AI thinking 显示",
        "invalid_input": "❌ 无效输入",
        "status_on": "开启",
        "status_off": "关闭",
        "error": "错误：{error}"
    },
    "English": {
        "goodbye": "👋 Goodbye!",
        "returning_menu": "🔄 Returning to main menu...\n",
        "main_title": "🎯 Multi-functional AI Assistant",
        "available_modes": "📋 Available Modes:",
        "mode_ai": "  1️⃣  AI Chat Mode - Chat with Ollama AI",
        "mode_map": "  2️⃣  Map Query Mode - Query address coordinates",
        "mode_settings": "  3️⃣  Settings - Configure language and display options",
        "tip_return": "💡 Tip: Enter 'return menu' to go back to main menu",
        "tip_exit": "       Enter 'exit' or 'quit' to exit program\n",
        "choose_mode": "Choose mode (number or name): ",
        "invalid_choice": "❌ Invalid choice, please try again\n",
        "thank_you": "👋 Thank you for using, goodbye!",
        "ai_mode_title": "🤖 AI Chat Mode Started - Model: {model}",
        "ai_mode_subtitle": "💬 You can start chatting with AI now!",
        "return_menu_tip": "📌 Enter 'return menu' to go back\n",
        "user_prompt": "User: ",
        "assistant_prompt": "\nAssistant: {answer}\n",
        "ai_thinking": "\n🤔 AI is thinking...\n",
        "map_mode_title": "🌍 Map Query Mode Started - OpenStreetMap Geocoding",
        "map_mode_subtitle": "📍 Enter address to get coordinates",
        "enter_address": "Enter address: ",
        "searching": "\n🔍 Searching: {address}",
        "query_success": "\n✅ Query successful!",
        "longitude": "📍 Longitude: {lon}",
        "latitude": "📍 Latitude: {lat}",
        "full_address": "📝 Full address: {addr}",
        "importance": "⭐ Match score: {imp:.2f}",
        "address_not_found": "\n❌ Address not found, please try a more specific address",
        "settings_title": "⚙️  Settings",
        "current_settings": "📋 Current Settings:",
        "setting_language": "  1️⃣  Language: {lang}",
        "setting_thinking": "  2️⃣  Show AI Thinking: {status}",
        "modify_tip": "💡 Enter number to modify settings, enter 'return menu' to go back\n",
        "choose_setting": "Choose setting to modify: ",
        "language_settings": "\n📝 Language Settings",
        "lang_option_cn": "  1. 中文 (Chinese)",
        "lang_option_en": "  2. English",
        "select_language": "\nSelect language (1/2): ",
        "switched_to_cn": "✅ 已切换到中文",
        "switched_to_en": "✅ Switched to English",
        "invalid_lang_choice": "❌ Invalid choice",
        "thinking_settings": "\n📝 AI Thinking Display Settings",
        "current_status": "  Current status: {status}",
        "enable_thinking": "\nEnable AI thinking display? (y/n): ",
        "thinking_enabled": "✅ AI thinking display enabled",
        "thinking_disabled": "✅ AI thinking display disabled",
        "invalid_input": "❌ Invalid input",
        "status_on": "On",
        "status_off": "Off",
        "error": "Error: {error}"
    }
}

def t(key: str, **kwargs) -> str:
    """
    获取当前语言的文本
    Args:
        key: 文本键
        **kwargs: 格式化参数
    Returns:
        格式化后的文本
    """
    lang = SETTINGS['language']
    text = TEXTS.get(lang, TEXTS["中文"]).get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text

def ask_qwen(prompt: str) -> str:
    """
    使用 OpenAI Client 方式调用本地 Ollama 模型
    Args:
        prompt: 用户输入的问题
    Returns:
        模型的回答
    """
    try:
        # 公共配置
        common_params = {
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "timeout": 120
        }
        
        # 如果开启了 thinking 显示，使用流式输出
        if SETTINGS['show_thinking']:
            print(t("ai_thinking"), end="", flush=True)
            response = client.chat.completions.create(**common_params, stream=True)
            
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_response += content
            print()  # 换行
            return full_response
        else:
            # 非流式输出
            response = client.chat.completions.create(**common_params, stream=False)
            return response.choices[0].message.content
    except Exception as e:
        return t("error", error=str(e))


def check_user_command(user_input: str) -> str:
    """
    检查用户输入的命令
    Args:
        user_input: 用户输入的字符串
    Returns:
        "exit" - 用户想退出程序
        "menu" - 用户想返回菜单
        "continue" - 继续处理用户输入
        "skip" - 空输入，跳过
    """
    if not user_input:
        return "skip"
    
    user_input_lower = user_input.lower()
    
    if user_input_lower in ("exit", "quit", "退出"):
        print(t("goodbye"))
        return "exit"
    
    if user_input_lower in ("返回菜单", "菜单", "menu", "back", "return menu"):
        print(t("returning_menu"))
        return "menu"
    
    return "continue"


def print_mode_header(title: str, subtitle: str = ""):
    """打印模式头部
    Args:
        title: 主标题
        subtitle: 副标题（可选）
    """
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    if subtitle:
        print(subtitle)
    print(t("return_menu_tip"))


def show_menu():
    """显示主菜单"""
    print("\n" + "=" * 60)
    print(t("main_title"))
    print("=" * 60)
    print(t("available_modes"))
    print(t("mode_ai"))
    print(t("mode_map"))
    print(t("mode_settings"))
    print("=" * 60)
    print(t("tip_return"))
    print(t("tip_exit"))


def ai_chat_mode():
    """AI 对话模式"""
    print_mode_header(
        t("ai_mode_title", model=MODEL_NAME),
        t("ai_mode_subtitle")
    )
    
    while True:
        user_input = input(t("user_prompt")).strip()
        
        command = check_user_command(user_input)
        if command in ("exit", "menu"):
            return command
        if command == "skip":
            continue
        
        answer = ask_qwen(user_input)
        # 如果开启了 thinking 显示，回答已经在流式输出中显示了
        if not SETTINGS['show_thinking']:
            print(t("assistant_prompt", answer=answer))
        else:
            print()  # 添加空行


def map_query_mode():
    """地图查询模式"""
    print_mode_header(
        t("map_mode_title"),
        t("map_mode_subtitle")
    )
    
    geocoder = NominatimGeocoder()
    
    while True:
        address = input(t("enter_address")).strip()
        
        command = check_user_command(address)
        if command in ("exit", "menu"):
            return command
        if command == "skip":
            continue
        
        print(t("searching", address=address))
        result = geocoder.geocode(address)
        
        if result:
            print(t("query_success"))
            print(t("longitude", lon=result['longitude']))
            print(t("latitude", lat=result['latitude']))
            print(t("full_address", addr=result['display_name']))
            print(t("importance", imp=result['importance']))
        else:
            print(t("address_not_found"))
        
        print("\n" + "-" * 50 + "\n")


def get_thinking_status() -> str:
    """获取 thinking 状态的显示文本"""
    return t("status_on") if SETTINGS['show_thinking'] else t("status_off")


def settings_mode():
    """设置模式"""
    def show_settings():
        """显示当前设置"""
        print("\n" + "=" * 60)
        print(t("settings_title"))
        print("=" * 60)
        print(t("current_settings"))
        print(t("setting_language", lang=SETTINGS['language']))
        print(t("setting_thinking", status=get_thinking_status()))
        print("=" * 60)
        print(t("modify_tip"))
    
    while True:
        show_settings()
        
        choice = input(t("choose_setting")).strip()
        
        command = check_user_command(choice)
        if command in ("exit", "menu"):
            return command
        if command == "skip":
            continue
        
        choice_lower = choice.lower()
        
        if choice_lower in ("1", "语言", "language"):
            print(t("language_settings"))
            print(t("lang_option_cn"))
            print(t("lang_option_en"))
            lang_choice = input(t("select_language")).strip()
            
            if lang_choice == "1":
                SETTINGS['language'] = "中文"
                print(t("switched_to_cn"))
            elif lang_choice == "2":
                SETTINGS['language'] = "English"
                print(t("switched_to_en"))
            else:
                print(t("invalid_lang_choice"))
        
        elif choice_lower in ("2", "thinking", "显示thinking"):
            print(t("thinking_settings"))
            print(t("current_status", status=get_thinking_status()))
            toggle = input(t("enable_thinking")).strip().lower()
            
            if toggle in ('y', 'yes', '是', '开启'):
                SETTINGS['show_thinking'] = True
                print(t("thinking_enabled"))
            elif toggle in ('n', 'no', '否', '关闭'):
                SETTINGS['show_thinking'] = False
                print(t("thinking_disabled"))
            else:
                print(t("invalid_input"))
        
        else:
            print(t("invalid_choice"))


def main():
    """主程序入口"""
    while True:
        show_menu()
        
        choice = input(t("choose_mode")).strip()
        
        if choice.lower() in ("exit", "quit", "退出"):
            break
        
        # 处理用户输入（转为小写进行匹配）
        choice_lower = choice.lower()
        if choice_lower in MODE_KEYWORDS["ai"]:
            result = ai_chat_mode()
        elif choice_lower in MODE_KEYWORDS["map"]:
            result = map_query_mode()
        elif choice_lower in MODE_KEYWORDS["settings"]:
            result = settings_mode()
        else:
            print(t("invalid_choice"))
            continue
        
        # 如果用户选择退出，则结束程序
        if result == "exit":
            break
    
    print(t("thank_you"))


if __name__ == "__main__":
    main()