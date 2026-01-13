import os
import readline  # 支持方向键、历史记录等输入增强功能
from openai import OpenAI
from dotenv import load_dotenv
from geocoding import NominatimGeocoder
from textD import TEXTS

# 加载环境变量
load_dotenv()

# 配置 readline 以支持更好的输入体验
# 启用 Tab 补全和历史记录功能
readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode emacs')  # Emacs 编辑模式（支持 Ctrl+A/E 等快捷键）

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

# 系统提示词 - Model-Based 模式理解（双语版本）
SYSTEM_PROMPT = """你是一个智能助手 / You are an intelligent assistant.

**功能 / Features:**
1. **AI对话 / AI Chat**: 与用户自然对话，回答问题 / Have natural conversations and answer questions
2. **地图查询 / Map Query**: 查询地址的经纬度坐标 / Query latitude and longitude coordinates
3. **语言切换 / Language Switch**: 切换界面语言（中文/English） / Switch interface language
4. **AI Thinking 开关 / Thinking Toggle**: 控制是否显示 AI 思考过程 / Control AI thinking display

**重要 / Important:**
- 用户可以用**中文或英文**发出任何指令，你都要能理解
- Users can give commands in **Chinese or English**, you must understand both
- 当用户说"切换到英文"、"change to english"、"switch to english"等，使用 switch_language 工具切换到 'en'
- 当用户说"切换到中文"、"change to chinese"、"switch to chinese"等，使用 switch_language 工具切换到 'cn'

**工具使用 / Tool Usage:**
- 查询位置/地址/坐标 → 使用 geocode_address 工具
- Query locations/addresses/coordinates → use geocode_address tool
- 切换语言（无论用什么语言表达）→ 使用 switch_language 工具
- Switch language (no matter which language used) → use switch_language tool
- 开关 thinking 显示 → 使用 toggle_thinking 工具
- Toggle thinking display → use toggle_thinking tool
- 退出/返回菜单 → 使用 navigate 工具
- Exit/return to menu → use navigate tool

请友好、准确地回应用户。Please respond in a friendly and accurate manner."""

# MCP 工具定义
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

LANGUAGE_TOOL = {
    "type": "function",
    "function": {
        "name": "switch_language",
        "description": "切换界面语言。Switch interface language.",
        "parameters": {
            "type": "object",
            "properties": {
                "language": {
                    "type": "string",
                    "enum": ["cn", "en"],
                    "description": "目标语言代码：'cn' 表示中文，'en' 表示 English"
                }
            },
            "required": ["language"]
        }
    }
}

THINKING_TOOL = {
    "type": "function",
    "function": {
        "name": "toggle_thinking",
        "description": "开关 AI thinking 显示。Toggle AI thinking display.",
        "parameters": {
            "type": "object",
            "properties": {
                "enabled": {
                    "type": "boolean",
                    "description": "true 表示开启，false 表示关闭"
                }
            },
            "required": ["enabled"]
        }
    }
}

NAVIGATE_TOOL = {
    "type": "function",
    "function": {
        "name": "navigate",
        "description": "导航控制：退出程序或返回菜单。Navigation control: exit program or return to menu.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["exit", "menu"],
                    "description": "'exit' 表示退出程序，'menu' 表示返回菜单"
                }
            },
            "required": ["action"]
        }
    }
}

TOOLS = [GEOCODING_TOOL, LANGUAGE_TOOL, THINKING_TOOL, NAVIGATE_TOOL]

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
    
    elif tool_name == "switch_language":
        lang = arguments.get("language", "cn")
        old_lang = SETTINGS['language']
        SETTINGS['language'] = lang
        
        lang_name = "中文" if lang == "cn" else "English"
        return json.dumps({
            "success": True,
            "old_language": old_lang,
            "new_language": lang,
            "message": f"✅ Switched to {lang_name}"
        }, ensure_ascii=False)
    
    elif tool_name == "toggle_thinking":
        enabled = arguments.get("enabled", False)
        SETTINGS['show_thinking'] = enabled
        
        status = t("status_on") if enabled else t("status_off")
        return json.dumps({
            "success": True,
            "thinking_enabled": enabled,
            "message": f"✅ AI Thinking {status}"
        }, ensure_ascii=False)
    
    elif tool_name == "navigate":
        action = arguments.get("action", "menu")
        return json.dumps({
            "success": True,
            "action": action,
            "message": "Navigation action recorded"
        }, ensure_ascii=False)
    
    return json.dumps({"error": f"Unknown tool: {tool_name}"}, ensure_ascii=False)

def ask_qwen(prompt: str, messages: list = None, use_tools: bool = False, use_system_prompt: bool = False) -> tuple:
    """
    使用 OpenAI Client 方式调用本地 Ollama 模型
    Args:
        prompt: 用户输入的问题
        messages: 对话历史（可选）
        use_tools: 是否启用工具调用
        use_system_prompt: 是否使用系统提示词（model-based 模式）
    Returns:
        (回答, 导航命令) - 导航命令可能是 None, "exit", "menu"
    """
    import json
    
    try:
        # 构建消息列表
        if messages is None:
            messages = []
            # 添加系统提示词
            if use_system_prompt:
                messages.append({"role": "system", "content": SYSTEM_PROMPT})
            messages.append({"role": "user", "content": prompt})
        
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
                    
                    # 根据不同工具显示不同的参数信息
                    if function_name == "geocode_address":
                        print(t("tool_query_address", address=function_args.get('address', '')))
                    elif function_name == "switch_language":
                        lang_name = "中文" if function_args.get('language') == 'cn' else "English"
                        print(f"🌐 切换到: {lang_name}")
                    elif function_name == "toggle_thinking":
                        status = "开启" if function_args.get('enabled') else "关闭"
                        print(f"🤔 AI Thinking: {status}")
                    elif function_name == "navigate":
                        action_text = "退出程序" if function_args.get('action') == 'exit' else "返回菜单"
                        print(f"🔄 操作: {action_text}")
                    
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
                
                # 检查是否有导航命令
                nav_action = None
                for result in tool_results:
                    result_data = json.loads(result)
                    if result_data.get("action") in ("exit", "menu"):
                        nav_action = result_data.get("action")
                
                # 使用工具结果再次调用模型生成最终回答
                final_response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    temperature=0.7,
                    timeout=120
                )
                return (final_response.choices[0].message.content, nav_action)
            
            return (message.content, None)
    except Exception as e:
        return (t("error", error=str(e)), None)


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


def ai_chat_mode():
    """AI 对话模式（Model-Based 智能理解）"""
    lang = SETTINGS['language']
    if lang == "cn":
        subtitle = t("ai_mode_subtitle") + "\n💡 我可以理解你的需求！你可以：\n   - 自然对话\n   - 查询地址坐标\n   - 切换语言（说'切换到英文'）\n   - 控制 thinking 显示（说'开启/关闭 thinking'）\n   - 随时说'退出'或'返回菜单'"
    else:
        subtitle = t("ai_mode_subtitle") + "\n💡 I can understand your needs! You can:\n   - Chat naturally\n   - Query address coordinates\n   - Switch language (say 'switch to Chinese')\n   - Control thinking display (say 'enable/disable thinking')\n   - Say 'exit' or 'return to menu' anytime"
    
    print_mode_header(
        t("ai_mode_title", model=MODEL_NAME) + " [Model-Based]",
        subtitle
    )
    
    # 初始化消息历史（包含系统提示词 - 双语版本）
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    while True:
        user_input = input(t("user_prompt")).strip()
        
        if not user_input:
            continue
        
        # 添加用户消息到历史
        messages.append({"role": "user", "content": user_input})
        
        # 使用 model-based 模式（带系统提示词和工具调用）
        answer, nav_action = ask_qwen(user_input, messages=messages.copy(), use_tools=True, use_system_prompt=False)
        
        # 检查导航命令
        if nav_action == "exit":
            print(t("goodbye"))
            return "exit"
        elif nav_action == "menu":
            print(t("returning_menu"))
            return "menu"
        
        # 添加助手回答到历史
        messages.append({"role": "assistant", "content": answer})
        
        # 显示回答
        if not SETTINGS['show_thinking']:
            print(t("assistant_prompt", answer=answer))
        else:
            print()  # 添加空行


def main():
    """主程序入口 - Model-Based 模式"""
    lang = SETTINGS['language']
    
    print("\n" + "=" * 60)
    if lang == "cn":
        print("🎯 智能助手 [Model-Based Mode]")
        print("💡 我可以理解你的自然语言指令！")
        print("\n你可以直接说：")
        print("  - '我想查询北京天安门的坐标'")
        print("  - '帮我查一下巴黎埃菲尔铁塔在哪里'")
        print("  - '切换到英文' 或 '切换语言'")
        print("  - '开启 thinking' 或 '关闭 thinking'")
        print("  - '退出' 或 'quit'")
        print("\n或者随便跟我聊天！")
    else:
        print("🎯 Intelligent Assistant [Model-Based Mode]")
        print("💡 I can understand your natural language commands!")
        print("\nYou can simply say:")
        print("  - 'I want to query the coordinates of Tiananmen Square'")
        print("  - 'Help me find where the Eiffel Tower in Paris is'")
        print("  - 'Switch to Chinese' or 'change language'")
        print("  - 'Enable thinking' or 'disable thinking'")
        print("  - 'Exit' or 'quit'")
        print("\nOr just chat with me!")
    print("=" * 60 + "\n")
    
    # 使用 AI 对话模式（model-based）
    result = ai_chat_mode()
    
    if result != "exit":
        print(t("thank_you"))


if __name__ == "__main__":
    main()