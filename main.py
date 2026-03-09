import os
import readline  # 支持方向键、历史记录等输入增强功能
from openai import OpenAI
from dotenv import load_dotenv
from geocoding import NominatimGeocoder
from weather import OpenMeteoWeather
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
3. **天气查询 / Weather Query**: 查询任何地点的天气信息和穿衣建议 / Query weather information and clothing advice for any location
4. **语言切换 / Language Switch**: 切换界面语言（中文/English） / Switch interface language
5. **AI Thinking 开关 / Thinking Toggle**: 控制是否显示 AI 思考过程 / Control AI thinking display

**🎯 语言一致性规则 (CRITICAL Language Consistency Rules):**
- **如果用户用中文提问** → 必须用纯中文回答（可在括号内补充英文）
- **If user asks in English** → Must reply in pure English ONLY (no Chinese mixed in)
- **当前系统语言设置**: 根据 current_language 参数
  - current_language='cn' → 回答用中文
  - current_language='en' → 回答用英文
- 禁止中英文混杂输出（如："天气 / Weather"，除非明确要求双语）

**重要 / Important:**
- 用户可以用**中文或英文**发出任何指令，你都要能理解
- Users can give commands in **Chinese or English**, you must understand both
- 当用户说"切换到英文"、"change to english"、"switch to english"等，使用 switch_language 工具切换到 'en'
- 当用户说"切换到中文"、"change to chinese"、"switch to chinese"等，使用 switch_language 工具切换到 'cn'

**工具使用 / Tool Usage:**
- 查询位置/地址/坐标 → 使用 geocode_address 工具
- Query locations/addresses/coordinates → use geocode_address tool
- 查询天气 → 使用 get_weather 工具（需要经纬度）
- Query weather → use get_weather tool (requires latitude/longitude)
- 切换语言（无论用什么语言表达）→ 使用 switch_language 工具
- Switch language (no matter which language used) → use switch_language tool
- 开关 thinking 显示 → 使用 toggle_thinking 工具
- Toggle thinking display → use toggle_thinking tool
- 退出/返回菜单 → 使用 navigate 工具
- Exit/return to menu → use navigate tool

**重要：串联使用工具 / Important: Chaining Tools:**
- 当用户问"某地的天气"或"去某地该穿什么"时，你需要：
  1. 先使用 geocode_address 获取该地的经纬度和完整地名
  2. 再使用 get_weather 查询天气信息
  3. 按照以下格式展示结果（清晰、结构化）
- When users ask about weather or clothing advice for a location:
  1. First use geocode_address to get coordinates and full location name
  2. Then use get_weather to query weather
  3. Present results in a clear, structured format

**天气信息展示格式规则 / Weather Display Format Rules:**

**中文用户 (Chinese Users):**
- 📍 查询地点: [完整地名]
- 🗺️ 坐标: (纬度, 经度)
- ☁️ 天气状况: [天气描述]
- 🌡️ 当天温度区间: [最低温]°C ~ [最高温]°C
- 🌡️ 当前温度: [温度]°C ([温度描述])
- 👔 出行建议: [穿衣建议]

**English Users:**
- 📍 Location: [Full location name]
- 🗺️ Coordinates: (latitude, longitude)
- ☁️ Weather: [Weather description]
- 🌡️ Today's Range: [min]°C ~ [max]°C
- 🌡️ Current: [temp]°C ([description])
- 👔 Travel Advice: [Clothing advice]

**示例 / Examples:**
- 中文: "北京今天天气怎么样？" → 纯中文回答
- English: "What's the weather in New York?" → Pure English response

请友好、准确地回应用户，并严格遵守语言一致性规则。
Please respond in a friendly and accurate manner, strictly following language consistency rules."""

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

WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "根据经纬度获取天气信息，包括当前天气、未来预报和穿衣建议。注意：需要先使用 geocode_address 获取经纬度。",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {
                    "type": "number",
                    "description": "纬度坐标，例如：39.9042（北京）"
                },
                "longitude": {
                    "type": "number",
                    "description": "经度坐标，例如：116.4074（北京）"
                },
                "forecast_days": {
                    "type": "integer",
                    "description": "预报天数（1-7天），默认为 3 天",
                    "default": 3
                }
            },
            "required": ["latitude", "longitude"]
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

TOOLS = [GEOCODING_TOOL, WEATHER_TOOL, LANGUAGE_TOOL, THINKING_TOOL, NAVIGATE_TOOL]

def detect_language(text: str) -> str:
    """
    检测用户输入的语言
    Args:
        text: 用户输入文本
    Returns:
        'cn' 或 'en'
    """
    # 统计中文字符数量
    chinese_chars = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
    # 统计英文字母数量
    english_chars = sum(1 for char in text if char.isalpha() and char.isascii())
    
    # 如果有中文字符，判断为中文
    if chinese_chars > 0:
        return 'cn'
    
    # 如果只有英文或其他字符，判断为英文
    return 'en'

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
    
    elif tool_name == "get_weather":
        latitude = arguments.get("latitude")
        longitude = arguments.get("longitude")
        forecast_days = arguments.get("forecast_days", 3)
        
        # 参数验证
        if latitude is None or longitude is None:
            return json.dumps({
                "success": False,
                "error": "Missing required parameters: latitude and longitude"
            }, ensure_ascii=False)
        
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (ValueError, TypeError):
            return json.dumps({
                "success": False,
                "error": f"Invalid coordinate values: latitude={latitude}, longitude={longitude}"
            }, ensure_ascii=False)
        
        # 范围检查
        if not (-90 <= latitude <= 90):
            return json.dumps({
                "success": False,
                "error": f"Latitude must be between -90 and 90, got {latitude}"
            }, ensure_ascii=False)
        
        if not (-180 <= longitude <= 180):
            return json.dumps({
                "success": False,
                "error": f"Longitude must be between -180 and 180, got {longitude}"
            }, ensure_ascii=False)
        
        weather_api = OpenMeteoWeather()
        result = weather_api.get_weather(latitude, longitude, forecast_days)
        
        if result:
            current = result["current"]
            forecast = result["forecast"][:forecast_days]
            
            # 获取当天的温度区间（从预报数据中获取）
            today_forecast = forecast[0] if forecast else None
            temp_range = None
            if today_forecast:
                temp_range = {
                    "min": today_forecast["temp_min"],
                    "max": today_forecast["temp_max"]
                }
            
            # 获取温度描述
            temp_description = weather_api.get_temperature_description(current["temperature"])
            
            # 获取穿衣建议和出行装备建议
            clothing_advice = weather_api.get_clothing_advice(
                current["temperature"],
                current["weather_code"]
            )
            
            return json.dumps({
                "success": True,
                "location": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "weather": {
                    "description": current["weather_description"],
                    "condition": current["weather_description"].split('/')[0].strip()
                },
                "temperature": {
                    "current": current["temperature"],
                    "description": temp_description,
                    "feels_like": current["feels_like"],
                    "range": temp_range
                },
                "details": {
                    "humidity": current["humidity"],
                    "wind_speed": current["wind_speed"],
                    "precipitation": current["precipitation"]
                },
                "travel_advice": {
                    "clothing": clothing_advice
                },
                "forecast": forecast
            }, ensure_ascii=False)
        else:
            return json.dumps({
                "success": False,
                "error": "Weather query failed"
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
                    timeout=120,
                    tools=TOOLS  # 保持工具定义，避免模型输出原始格式
                )
                
                final_message = final_response.choices[0].message
                
                # 检查模型是否再次尝试调用工具（处理工具调用循环）
                if hasattr(final_message, 'tool_calls') and final_message.tool_calls:
                    # 模型想要继续调用工具，递归处理（最多2轮）
                    for tool_call in final_message.tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)
                        
                        print("\n" + t("tool_calling", tool=function_name))
                        result = execute_tool(function_name, function_args)
                        
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
                    
                    # 第三次调用生成最终回答
                    final_response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=messages,
                        temperature=0.7,
                        timeout=120
                    )
                    final_message = final_response.choices[0].message
                
                # 检查响应内容是否有效
                if not final_message.content:
                    return ("⚠️ 模型未返回有效响应，请重试", nav_action)
                
                return (final_message.content, nav_action)
            
            return (message.content, None)
    except TimeoutError as e:
        error_msg = "⏱️ 请求超时，请检查 Ollama 服务是否正常运行"
        print(f"\n❌ {error_msg}")
        return (error_msg, None)
    except ConnectionError as e:
        error_msg = ("🔌 无法连接到 Ollama 服务，请确认:\n"
                    "   1. Ollama 已安装并运行 (运行 'ollama serve')\n"
                    "   2. 服务地址正确 (默认: http://localhost:11434)")
        print(f"\n❌ {error_msg}")
        return (error_msg, None)
    except json.JSONDecodeError as e:
        error_msg = f"📦 JSON 解析错误: {str(e)}"
        print(f"\n❌ {error_msg}")
        return (error_msg, None)
    except KeyError as e:
        error_msg = f"🔑 缺少必要的响应字段: {str(e)}"
        print(f"\n❌ {error_msg}")
        return (error_msg, None)
    except Exception as e:
        import traceback
        error_msg = f"❌ 未知错误: {str(e)}"
        print(f"\n{error_msg}")
        print(f"\n🐛 详细错误信息:\n{traceback.format_exc()}")
        return (error_msg, None)


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
        
        # 检测用户输入语言并自动切换
        detected_lang = detect_language(user_input)
        if detected_lang != SETTINGS['language']:
            SETTINGS['language'] = detected_lang
            print(f"\n🌐 {t('lang_auto_switch')}: {'中文' if detected_lang == 'cn' else 'English'}\n")
        
        # 添加用户消息到历史
        messages.append({"role": "user", "content": user_input})
        
        # 在系统提示词中注入当前语言设置
        current_system_prompt = SYSTEM_PROMPT.replace(
            "**🎯 语言一致性规则",
            f"**[Current System Language: {'Chinese' if SETTINGS['language'] == 'cn' else 'English'}]**\n\n**🎯 语言一致性规则"
        )
        messages[0] = {"role": "system", "content": current_system_prompt}
        
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
        print("  - '切换到英文' 或 'change language'")
        print("  - '开启 thinking' 或 '关闭 thinking'")
        print("  - '退出' 或 'quit'")
        print("\n或者随便跟我聊天！")
    else:
        print("🎯 Intelligent Assistant [Model-Based Mode]")
        print("💡 I can understand your natural language commands!")
        print("\nYou can simply say:")
        print("  - 'I want to query the coordinates of Tiananmen Square'")
        print("  - 'Help me find where the Eiffel Tower in Paris is'")
        print("  - 'Switch to Chinese' or '切换语言'")
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