"""
文本字典 - text dictionary
多语言文本配置文件
Internationalization text configuration

数据结构说明：
- 第一级：功能关键词（key）
- 第二级：语言代码（cn=中文, en=English）
- 支持格式化参数：使用 {param_name} 占位符
"""

# 多语言文本字典 - 第一级为关键词，第二级为语言代码（cn/en）
TEXTS = {
    "goodbye": {"cn": "👋 再见！", "en": "👋 Goodbye!"},
    "returning_menu": {"cn": "🔄 正在返回主菜单...\n", "en": "🔄 Returning to main menu...\n"},
    "main_title": {"cn": "🎯 多功能智能助手", "en": "🎯 Multi-functional AI Assistant"},
    "available_modes": {"cn": "📋 可用模式：", "en": "📋 Available Modes:"},
    "mode_ai": {"cn": "  1️⃣  AI对话模式 - 与 Ollama AI 进行对话", "en": "  1️⃣  AI Chat Mode - Chat with Ollama AI"},
    "mode_map": {"cn": "  2️⃣  地图查询模式 - 查询地址的经纬度坐标", "en": "  2️⃣  Map Query Mode - Query address coordinates"},
    "mode_settings": {"cn": "  3️⃣  设置 - 配置语言和显示选项", "en": "  3️⃣  Settings - Configure language and display options"},
    "tip_return": {"cn": "💡 提示：在任意模式中输入 '返回菜单' 可返回主菜单", "en": "💡 Tip: Enter 'return menu' to go back to main menu"},
    "tip_exit": {"cn": "       输入 'exit' 或 'quit' 可退出程序\n", "en": "       Enter 'exit' or 'quit' to exit program\n"},
    "choose_mode": {"cn": "请选择模式（输入数字或模式名称）：", "en": "Choose mode (number or name): "},
    "invalid_choice": {"cn": "❌ 无效的选择，请重新输入\n", "en": "❌ Invalid choice, please try again\n"},
    "thank_you": {"cn": "👋 感谢使用，再见！", "en": "👋 Thank you for using, goodbye!"},
    "ai_mode_title": {"cn": "🤖 AI对话模式已启动 - 模型: {model}", "en": "🤖 AI Chat Mode Started - Model: {model}"},
    "ai_mode_subtitle": {"cn": "💬 你可以开始与 AI 对话了！", "en": "💬 You can start chatting with AI now!"},
    "return_menu_tip": {"cn": "📌 输入 '返回菜单' 返回主菜单\n", "en": "📌 Enter 'return menu' to go back\n"},
    "user_prompt": {"cn": "User：", "en": "User: "},
    "assistant_prompt": {"cn": "\nAssistant：{answer}\n", "en": "\nAssistant: {answer}\n"},
    "ai_thinking": {"cn": "\n🤔 AI 正在思考...\n", "en": "\n🤔 AI is thinking...\n"},
    "map_mode_title": {"cn": "🌍 地图查询模式已启动 - OpenStreetMap 地理编码", "en": "🌍 Map Query Mode Started - OpenStreetMap Geocoding"},
    "map_mode_subtitle": {"cn": "📍 输入地址获取经纬度坐标", "en": "📍 Enter address to get coordinates"},
    "enter_address": {"cn": "请输入地址: ", "en": "Enter address: "},
    "searching": {"cn": "\n🔍 正在查询: {address}", "en": "\n🔍 Searching: {address}"},
    "query_success": {"cn": "\n✅ 查询成功！", "en": "\n✅ Query successful!"},
    "longitude": {"cn": "📍 经度 (Longitude): {lon}", "en": "📍 Longitude: {lon}"},
    "latitude": {"cn": "📍 纬度 (Latitude): {lat}", "en": "📍 Latitude: {lat}"},
    "full_address": {"cn": "📝 完整地址: {addr}", "en": "📝 Full address: {addr}"},
    "importance": {"cn": "⭐ 匹配度: {imp:.2f}", "en": "⭐ Match score: {imp:.2f}"},
    "address_not_found": {"cn": "\n❌ 未找到该地址，请尝试更具体的地址", "en": "\n❌ Address not found, please try a more specific address"},
    "settings_title": {"cn": "⚙️  设置 / Settings", "en": "⚙️  Settings"},
    "current_settings": {"cn": "📋 当前设置：", "en": "📋 Current Settings:"},
    "setting_language": {"cn": "  1️⃣  语言 / Language: {lang}", "en": "  1️⃣  Language: {lang}"},
    "setting_thinking": {"cn": "  2️⃣  显示 AI Thinking: {status}", "en": "  2️⃣  Show AI Thinking: {status}"},
    "modify_tip": {"cn": "💡 输入数字修改设置，输入 '返回菜单' 返回\n", "en": "💡 Enter number to modify settings, enter 'return menu' to go back\n"},
    "choose_setting": {"cn": "请选择要修改的设置：", "en": "Choose setting to modify: "},
    "language_settings": {"cn": "\n📝 语言设置 / Language Settings", "en": "\n📝 Language Settings"},
    "lang_option_cn": {"cn": "  1. 中文", "en": "  1. 中文 (Chinese)"},
    "lang_option_en": {"cn": "  2. English", "en": "  2. English"},
    "select_language": {"cn": "\n请选择语言 / Select language (1/2): ", "en": "\nSelect language (1/2): "},
    "switched_to_cn": {"cn": "✅ 已切换到中文", "en": "✅ 已切换到中文"},
    "switched_to_en": {"cn": "✅ Switched to English", "en": "✅ Switched to English"},
    "invalid_lang_choice": {"cn": "❌ 无效选择 / Invalid choice", "en": "❌ Invalid choice"},
    "thinking_settings": {"cn": "\n📝 AI Thinking 显示设置", "en": "\n📝 AI Thinking Display Settings"},
    "current_status": {"cn": "  当前状态: {status}", "en": "  Current status: {status}"},
    "enable_thinking": {"cn": "\n是否开启显示 AI thinking 过程？(y/n): ", "en": "\nEnable AI thinking display? (y/n): "},
    "thinking_enabled": {"cn": "✅ 已开启 AI thinking 显示", "en": "✅ AI thinking display enabled"},
    "thinking_disabled": {"cn": "✅ 已关闭 AI thinking 显示", "en": "✅ AI thinking display disabled"},
    "invalid_input": {"cn": "❌ 无效输入", "en": "❌ Invalid input"},
    "status_on": {"cn": "开启", "en": "On"},
    "status_off": {"cn": "关闭", "en": "Off"},
    "error": {"cn": "错误：{error}", "en": "Error: {error}"},
    "ai_tool_hint": {"cn": "💡 你可以问我关于地址和位置的问题，我会自动查询地理信息！", "en": "💡 You can ask me about addresses and locations, I'll query geographic information automatically!"},
    "tool_calling": {"cn": "🔧 正在调用工具: {tool}", "en": "🔧 Calling tool: {tool}"},
    "tool_query_address": {"cn": "📍 查询地址: {address}", "en": "📍 Query address: {address}"},
    "tool_query_weather": {"cn": "🌤️  查询天气: ({lat}, {lon})", "en": "🌤️  Query weather: ({lat}, {lon})"},
    "tool_switch_lang": {"cn": "🌐 切换到: {lang}", "en": "🌐 Switch to: {lang}"},
    "tool_thinking_status": {"cn": "🤔 AI Thinking: {status}", "en": "🤔 AI Thinking: {status}"},
    "tool_navigation": {"cn": "🔄 操作: {action}", "en": "🔄 Action: {action}"},
    "lang_auto_switch": {"cn": "自动切换语言", "en": "Language auto-switched"},
    "action_exit": {"cn": "退出程序", "en": "Exit program"},
    "action_menu": {"cn": "返回菜单", "en": "Return to menu"},
    "lang_name_cn": {"cn": "中文", "en": "Chinese"},
    "lang_name_en": {"cn": "English", "en": "English"},
    "error_timeout": {"cn": "⏱️ 请求超时，请检查 Ollama 服务是否正常运行", "en": "⏱️ Request timeout, please check if Ollama service is running"},
    "error_connection": {"cn": "🔌 无法连接到 Ollama 服务，请确认:\n   1. Ollama 已安装并运行 (运行 'ollama serve')\n   2. 服务地址正确 (默认: http://localhost:11434)", "en": "🔌 Cannot connect to Ollama service, please confirm:\n   1. Ollama is installed and running (run 'ollama serve')\n   2. Service address is correct (default: http://localhost:11434)"},
    "error_json": {"cn": "📦 JSON 解析错误: {error}", "en": "📦 JSON parse error: {error}"},
    "error_keyerror": {"cn": "🔑 缺少必要的响应字段: {error}", "en": "🔑 Missing required response field: {error}"},
    "error_unknown": {"cn": "❌ 未知错误: {error}", "en": "❌ Unknown error: {error}"},
    "error_details": {"cn": "🐛 详细错误信息:\n{trace}", "en": "🐛 Detailed error:\n{trace}"},
    "error_no_response": {"cn": "⚠️ 模型未返回有效响应，请重试", "en": "⚠️ Model returned no valid response, please retry"},
    "ai_chat_tips_cn": {"cn": "\n💡 我可以理解你的需求！你可以：\n   - 自然对话\n   - 查询地址坐标\n   - 切换语言（说'切换到英文'）\n   - 控制 thinking 显示（说'开启/关闭 thinking'）\n   - 随时说'退出'或'返回菜单'", "en": ""},
    "ai_chat_tips_en": {"cn": "", "en": "\n💡 I can understand your needs! You can:\n   - Chat naturally\n   - Query address coordinates\n   - Switch language (say 'switch to Chinese')\n   - Control thinking display (say 'enable/disable thinking')\n   - Say 'exit' or 'return to menu' anytime"},
    "welcome_title": {"cn": "🎯 智能助手 [Model-Based Mode]", "en": "🎯 Intelligent Assistant [Model-Based Mode]"},
    "welcome_subtitle": {"cn": "💡 我可以理解你的自然语言指令！", "en": "💡 I can understand your natural language commands!"},
    "welcome_prompt": {"cn": "\n你可以直接说：", "en": "\nYou can simply say:"},
    "welcome_examples_cn": {"cn": "  - '我想查询北京天安门的坐标'\n  - '帮我查一下巴黎埃菲尔铁塔在哪里'\n  - '切换到英文' 或 'change language'\n  - '开启 thinking' 或 '关闭 thinking'\n  - '退出' 或 'quit'\n\n或者随便跟我聊天！", "en": ""},
    "welcome_examples_en": {"cn": "", "en": "  - 'I want to query the coordinates of Tiananmen Square'\n  - 'Help me find where the Eiffel Tower in Paris is'\n  - 'Switch to Chinese' or '切换语言'\n  - 'Enable thinking' or 'disable thinking'\n  - 'Exit' or 'quit'\n\nOr just chat with me!"},
    "weather_location": {"cn": "📍 查询地点", "en": "📍 Location"},
    "weather_coordinates": {"cn": "🗺️  坐标", "en": "🗺️  Coordinates"},
    "weather_condition": {"cn": "☁️  天气状况", "en": "☁️  Weather Condition"},
    "weather_temp_range": {"cn": "🌡️  当天温度区间", "en": "🌡️  Today's Temperature Range"},
    "weather_current_temp": {"cn": "🌡️  当前温度", "en": "🌡️  Current Temperature"},
    "weather_travel_advice": {"cn": "👔 出行建议", "en": "👔 Travel Advice"},
    "weather_feels_like": {"cn": "🤔 体感温度: {temp}°C", "en": "🤔 Feels like: {temp}°C"},
    "weather_humidity": {"cn": "💧 湿度: {humidity}%", "en": "💧 Humidity: {humidity}%"},
    "weather_wind": {"cn": "💨 风速: {speed} km/h", "en": "💨 Wind: {speed} km/h"},
    "weather_precipitation": {"cn": "🌧️  降水: {precip} mm", "en": "🌧️  Precipitation: {precip} mm"},
    "weather_forecast": {"cn": "📅 未来预报", "en": "📅 Forecast"}
}

# 支持的语言列表
SUPPORTED_LANGUAGES = ["cn", "en"]

# 默认语言
DEFAULT_LANGUAGE = "cn"
