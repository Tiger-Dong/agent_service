import os
from openai import OpenAI
from dotenv import load_dotenv
from geocoding import NominatimGeocoder
from textD import TEXTS

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
    "language": "cn",  # 可选: "cn", "en"
    "show_thinking": False  # 是否显示 AI thinking 过程
}

# 模式匹配关键词
MODE_KEYWORDS = {
    "ai": ("1", "ai对话模式", "ai对话", "ai", "对话模式", "对话", "ai chat", "chat"),
    "map": ("2", "地图查询模式", "地图查询", "地图模式", "地图", "查询模式", "查询", "map", "query"),
    "settings": ("3", "设置", "settings", "配置", "setting")
}

# MCP 工具定义 - 地理编码工具
GEOCODING_TOOL = {
    "type": "function",
    "function": {
        "name": "geocode_address",
        "description": "将地址转换为经纬度坐标。可以查询世界各地的地址，包括中文地址。返回经纬度、完整地址和匹配度信息。",
        "parameters": {
            "type": "object",
            "properties": {
                "address": {
                    "type": "string",
                    "description": "要查询的地址，可以是中文或英文地址，例如：'北京天安门'、'Eiffel Tower, Paris'"
                }
            },
            "required": ["address"]
        }
    }
}

TOOLS = [GEOCODING_TOOL]

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
    text = TEXTS.get(key, {}).get(lang, key)
    if kwargs:
        return text.format(**kwargs)
    return text

def execute_tool(tool_name: str, arguments: dict) -> str:
    """
    执行工具调用
    Args:
        tool_name: 工具名称
        arguments: 工具参数
    Returns:
        工具执行结果（JSON 字符串）
    """
    import json
    
    if tool_name == "geocode_address":
        address = arguments.get("address", "")
        geocoder = NominatimGeocoder()
        result = geocoder.geocode(address)
        
        if result:
            return json.dumps({
                "success": True,
                "address": address,
                "longitude": result['longitude'],
                "latitude": result['latitude'],
                "display_name": result['display_name'],
                "importance": result['importance']
            }, ensure_ascii=False)
        else:
            return json.dumps({
                "success": False,
                "address": address,
                "error": "Address not found"
            }, ensure_ascii=False)
    
    return json.dumps({"error": f"Unknown tool: {tool_name}"}, ensure_ascii=False)

def ask_qwen(prompt: str, messages: list = None, use_tools: bool = False) -> str:
    """
    使用 OpenAI Client 方式调用本地 Ollama 模型
    Args:
        prompt: 用户输入的问题
        messages: 对话历史（可选）
        use_tools: 是否启用工具调用
    Returns:
        模型的回答
    """
    import json
    
    try:
        # 构建消息列表
        if messages is None:
            messages = [{"role": "user", "content": prompt}]
        
        # 公共配置
        common_params = {
            "model": MODEL_NAME,
            "messages": messages,
            "temperature": 0.7,
            "timeout": 120
        }
        
        # 如果启用工具，添加工具定义
        if use_tools:
            common_params["tools"] = TOOLS
        
        # 如果开启了 thinking 显示，使用流式输出
        if SETTINGS['show_thinking'] and not use_tools:
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
            message = response.choices[0].message
            
            # 检查是否有工具调用
            if use_tools and hasattr(message, 'tool_calls') and message.tool_calls:
                tool_results = []
                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # 显示工具调用信息
                    print("\n" + t("tool_calling", tool=function_name))
                    print(t("tool_query_address", address=function_args.get('address', '')))
                    
                    # 执行工具
                    result = execute_tool(function_name, function_args)
                    tool_results.append(result)
                    
                    # 将工具调用和结果添加到消息历史
                    messages.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [{
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": function_name,
                                "arguments": tool_call.function.arguments
                            }
                        }]
                    })
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })
                
                # 使用工具结果再次调用模型生成最终回答
                final_response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    temperature=0.7,
                    timeout=120
                )
                return final_response.choices[0].message.content
            
            return message.content
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
    """AI 对话模式（支持 MCP 工具调用）"""
    subtitle = t("ai_mode_subtitle") + "\n" + t("ai_tool_hint")
    
    print_mode_header(
        t("ai_mode_title", model=MODEL_NAME),
        subtitle
    )
    
    messages = []
    
    while True:
        user_input = input(t("user_prompt")).strip()
        
        command = check_user_command(user_input)
        if command in ("exit", "menu"):
            return command
        if command == "skip":
            continue
        
        # 添加用户消息到历史
        messages.append({"role": "user", "content": user_input})
        
        # 使用工具调用模式
        answer = ask_qwen(user_input, messages=messages.copy(), use_tools=True)
        
        # 添加助手回答到历史
        messages.append({"role": "assistant", "content": answer})
        
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
                SETTINGS['language'] = "cn"
                print(t("switched_to_cn"))
            elif lang_choice == "2":
                SETTINGS['language'] = "en"
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