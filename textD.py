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
    # 基本交互
    "goodbye": {"cn": "👋 再见！", "en": "👋 Goodbye!"},
    "returning_menu": {"cn": "🔄 正在返回主菜单...\n", "en": "🔄 Returning to main menu...\n"},
    "thank_you": {"cn": "👋 感谢使用，再见！", "en": "👋 Thank you for using, goodbye!"},
    "user_prompt": {"cn": "User：", "en": "User: "},
    "assistant_prompt": {"cn": "\nAssistant：{answer}\n", "en": "\nAssistant: {answer}\n"},
    "ai_thinking": {"cn": "\n🤔 AI 正在思考...\n", "en": "\n🤔 AI is thinking...\n"},
    
    # AI 对话模式
    "ai_mode_title": {"cn": "🤖 AI对话模式已启动 - 模型: {model}", "en": "🤖 AI Chat Mode Started - Model: {model}"},
    "ai_mode_subtitle": {"cn": "💬 你可以开始与 AI 对话了！", "en": "💬 You can start chatting with AI now!"},
    "return_menu_tip": {"cn": "📌 输入 '返回菜单' 返回主菜单\n", "en": "📌 Enter 'return menu' to go back\n"},
    "ai_chat_tips_cn": {"cn": "\n💡 我可以理解你的需求！你可以：\n   - 自然对话\n   - 查询地址坐标\n   - 切换语言（说'切换到英文'）\n   - 控制 thinking 显示（说'开启/关闭 thinking'）\n   - 随时说'退出'或'返回菜单'", "en": ""},
    "ai_chat_tips_en": {"cn": "", "en": "\n💡 I can understand your needs! You can:\n   - Chat naturally\n   - Query address coordinates\n   - Switch language (say 'switch to Chinese')\n   - Control thinking display (say 'enable/disable thinking')\n   - Say 'exit' or 'return to menu' anytime"},
    
    # 欢迎消息
    "welcome_title": {"cn": "🎯 智能助手 [Model-Based Mode]", "en": "🎯 Intelligent Assistant [Model-Based Mode]"},
    "welcome_subtitle": {"cn": "💡 我可以理解你的自然语言指令！", "en": "💡 I can understand your natural language commands!"},
    "welcome_prompt": {"cn": "\n你可以直接说：", "en": "\nYou can simply say:"},
    "welcome_examples_cn": {"cn": "  - '我想查询北京天安门的坐标'\n  - '帮我查一下巴黎埃菲尔铁塔在哪里'\n  - '切换到英文' 或 'change language'\n  - '开启 thinking' 或 '关闭 thinking'\n  - '退出' 或 'quit'\n\n或者随便跟我聊天！", "en": ""},
    "welcome_examples_en": {"cn": "", "en": "  - 'I want to query the coordinates of Tiananmen Square'\n  - 'Help me find where the Eiffel Tower in Paris is'\n  - 'Switch to Chinese' or '切换语言'\n  - 'Enable thinking' or 'disable thinking'\n  - 'Exit' or 'quit'\n\nOr just chat with me!"},
    
    # 工具调用显示
    "tool_calling": {"cn": "🔧 正在调用工具: {tool}", "en": "🔧 Calling tool: {tool}"},
    "tool_query_address": {"cn": "📍 查询地址: {address}", "en": "📍 Query address: {address}"},
    "tool_switch_lang": {"cn": "🌐 切换到: {lang}", "en": "🌐 Switch to: {lang}"},
    "tool_thinking_status": {"cn": "🤔 AI Thinking: {status}", "en": "🤔 AI Thinking: {status}"},
    "tool_navigation": {"cn": "🔄 操作: {action}", "en": "🔄 Action: {action}"},
    
    # 工具参数
    "action_exit": {"cn": "退出程序", "en": "Exit program"},
    "action_menu": {"cn": "返回菜单", "en": "Return to menu"},
    "lang_name_cn": {"cn": "中文", "en": "Chinese"},
    "lang_name_en": {"cn": "English", "en": "English"},
    "status_on": {"cn": "开启", "en": "On"},
    "status_off": {"cn": "关闭", "en": "Off"},
    
    # 错误消息
    "error_timeout": {"cn": "⏱️ 请求超时，请检查 Ollama 服务是否正常运行", "en": "⏱️ Request timeout, please check if Ollama service is running"},
    "error_connection": {"cn": "🔌 无法连接到 Ollama 服务，请确认:\n   1. Ollama 已安装并运行 (运行 'ollama serve')\n   2. 服务地址正确 (默认: http://localhost:11434)", "en": "🔌 Cannot connect to Ollama service, please confirm:\n   1. Ollama is installed and running (run 'ollama serve')\n   2. Service address is correct (default: http://localhost:11434)"},
    "error_json": {"cn": "📦 JSON 解析错误: {error}", "en": "📦 JSON parse error: {error}"},
    "error_keyerror": {"cn": "🔑 缺少必要的响应字段: {error}", "en": "🔑 Missing required response field: {error}"},
    "error_unknown": {"cn": "❌ 未知错误: {error}", "en": "❌ Unknown error: {error}"},
    "error_details": {"cn": "🐛 详细错误信息:\n{trace}", "en": "🐛 Detailed error:\n{trace}"},
    "error_no_response": {"cn": "⚠️ 模型未返回有效响应，请重试", "en": "⚠️ Model returned no valid response, please retry"},
}

# 支持的语言列表
SUPPORTED_LANGUAGES = ["cn", "en"]

# 默认语言
DEFAULT_LANGUAGE = "cn"
