# Agent Service - Model-Based AI Assistant

基于 Ollama 的智能对话助手（Model-Based 架构 + MCP 工具调用）

---



## 功能特性

### 🎯 Model-Based 智能架构
- **自然语言理解**：无需记忆命令，用人类自然语言交流即可
- **意图自动识别**：AI 理解你的需求并自动调用相应工具
- **零学习成本**：像和朋友聊天一样使用所有功能

### 🔧 MCP 工具调用系统
基于 Model Context Protocol (MCP) 实现的 5 大智能工具：

- **geocode_address** - 地理编码（查询地址坐标）
- **get_weather** - 天气查询（实时天气 + 穿衣建议）
- **switch_language** - 语言切换（中文/English）
- **toggle_thinking** - AI 思考过程开关
- **navigate** - 导航控制（退出/返回）

### 💬 核心特性
- 📝 **对话历史记忆**：支持多轮上下文理解
- 🔌 **多模型支持**：兼容 Qwen、Llama 等 Ollama 模型
- 🌐 **双语界面**：中英文实时切换
- 💡 **思考可视化**：可选显示 AI 逐字生成过程
- 🗺️ **地理编码**：支持全球地址查询
- 🌤️ **天气查询**：实时天气信息和智能穿衣建议

## 环境要求

- Python 3.8+
- uv（Python 包管理器）
- Ollama 服务

## 安装步骤

1. 克隆项目
```bash
git clone https://github.com/Tiger-Dong/agent_service.git
cd agent_service
```

2. 安装 uv（如果还没有）
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或使用 Homebrew
brew install uv
```

3. 安装项目依赖
```bash
# uv 会自动创建虚拟环境并安装依赖
uv sync
```

4. 配置环境变量（可选）
```bash
cp .env.example .env
# 如需修改配置，编辑 .env 文件
```

5. 安装并启动 Ollama
```bash
# 下载模型
ollama pull qwen3:8b

# 启动服务
ollama serve
```

## 使用方法

启动智能助手：

```bash
# 使用 uv 运行（推荐）
uv run python main.py

# 或先激活虚拟环境
source .venv/bin/activate
python main.py
```

启动后使用自然语言与 AI 交互即可。

**📖 详细使用指南：** 请查看 **[instruction.md](instruction.md)** 了解完整的使用流程、技巧和常见问题。

## 📖 功能使用示例

本项目采用 **Model-Based** 架构，使用自然语言交互，无需记忆命令。AI 会自动理解你的意图并调用相应工具。

### 💡 功能示例

#### 1. 查询地理位置

```bash
User：帮我查一下巴黎埃菲尔铁塔的坐标

🔧 正在调用工具: geocode_address
📍 查询地址: 巴黎埃菲尔铁塔

Assistant：巴黎埃菲尔铁塔的坐标如下：
- 经度：2.2945°
- 纬度：48.8580°
- 完整地址：Tour Eiffel, Avenue Gustave Eiffel, Paris 75007, France
```

**其他表达方式：** "北京天安门在哪里？" / "Where is the Eiffel Tower?" / "东京的经纬度"

#### 2. 查询天气和穿衣建议 ⭐ NEW

```bash
User：北京今天天气怎么样？

🔧 正在调用工具: geocode_address
📍 查询地址: 北京

🔧 正在调用工具: get_weather
🌤️  查询天气: (39.9042, 116.4074)

Assistant：北京今天的天气信息如下：

📍 查询地点 (Location): 北京市, 中国
🗺️  坐标 (Coordinates): (39.9042, 116.4074)
☁️  天气状况 (Weather): 晴天 / Clear sky
🌡️  当天温度区间 (Today's Range): -5.7°C ~ 1.4°C
🌡️  当前温度 (Current): -5.2°C (冰点以下 / Below freezing)
    体感温度 (Feels like): -8.9°C

👔 出行建议 (Travel Advice):
    • 寒冷，建议穿厚外套、毛衣、长裤
    • Cold - thick coat, sweater, long pants

💧 湿度 (Humidity): 60%
💨 风速 (Wind): 2.7 km/h
```
- 天气：基本晴朗 / Mainly clear
```

**其他表达方式：** 
- "北京今天天气怎么样？"
- "达拉斯和休斯顿明天哪个更冷？"
- "What's the weather in Tokyo?"
- "去吉林需要穿羽绒服吗？"

#### 3. 切换语言

```bash
User：切换到英文

🔧 正在调用工具: switch_language
Assistant：✅ Language has been switched to English.
```

**其他表达方式：** "我想用英文" / "change language to English" / "切换语言"

#### 4. 控制思考过程显示

```bash
User：开启 thinking

🔧 正在调用工具: toggle_thinking
Assistant：✅ 已开启 AI thinking 显示功能。
从现在开始，你可以看到我逐字生成回答的过程。
```

**其他表达方式：** "我想看思考过程" / "enable thinking" / "关闭 thinking" / "disable thinking"

#### 5. 退出程序

**示例：** "退出" / "exit" / "bye" / "goodbye"

### 🎨 多轮对话示例（包含天气查询）

```bash
User：帮我查一下北京的坐标
Assistant：北京的坐标信息如下：经度 116.4074°，纬度 39.9042°

User：那里今天天气怎么样？
🔧 正在调用工具: get_weather
Assistant：北京今天的天气：
- 温度：-2°C，体感 -5°C
- 天气：晴天 / Clear sky
- 建议：寒冷，建议穿厚外套、毛衣、长裤

User：那上海呢？
Assistant：上海的坐标信息如下：经度 121.4737°，纬度 31.2304°

User：上海明天穿什么？
🔧 正在调用工具: get_weather
Assistant：上海明天的天气预报：
- 温度：8°C ~ 15°C
- 天气：局部多云
- 建议：温和，建议穿长袖衬衫、薄外套

User：切换到英文
Assistant：✅ Successfully switched to English.

User：What about Tokyo weather?
🔧 Calling tool: geocode_address
🔧 Calling tool: get_weather
Assistant：Tokyo weather today:
- Temperature: 10°C, feels like 8°C
- Weather: Mainly clear
- Suggestion: Cool - jacket, hoodie, long pants

User：exit
Assistant：👋 Goodbye!
```

## 项目结构

```
agent_service/
├── main.py                  # 主程序（Model-Based 架构 + MCP 工具系统）
│   ├── SYSTEM_PROMPT       # AI 意图理解的系统提示词（中英双语）
│   ├── TOOLS               # 5 个 MCP 工具定义（geocode/weather/language/thinking/navigate）
│   ├── execute_tool()      # 统一工具执行函数
│   ├── ask_qwen()          # AI 调用函数（支持工具调用）
│   └── ai_chat_mode()      # Model-Based 对话模式
├── textD.py                 # 多语言文本字典（keyword→language 结构）
├── geocoding.py             # 地理编码模块（OpenStreetMap Nominatim）
├── geocoding_examples.py    # 地理编码使用示例
├── weather.py               # 天气查询模块（Open-Meteo API）
├── weather_examples.py      # 天气模块使用示例
├── requirements.txt         # Python 依赖列表
├── .env                     # 环境变量配置（不上传到 Git）
├── .env.example             # 环境变量模板
├── README.md                # 项目说明文档
└── .gitignore              # Git 忽略配置
```

## 🔧 扩展工具

添加新工具只需 3 步：
1. 在 `main.py` 定义工具 Schema
2. 在 `execute_tool()` 实现逻辑
3. 在 `SYSTEM_PROMPT` 告诉 AI 何时使用

## 配置说明

`.env` 文件配置项：
- `OLLAMA_BASE_URL`: Ollama API 地址（默认：http://localhost:11434/v1）
- `OLLAMA_API_KEY`: API Key（Ollama 不验证，但必须提供）
- `MODEL_NAME`: 使用的模型名称（默认：qwen3:8b）

## 💡 常见问题

**Q: 地址查询失败？**
使用更具体的地址："北京天安门" 而不是 "天安门"

**Q: 更换模型？**
修改 `.env` 中的 `MODEL_NAME=llama3:8b`

**Q: 快捷键？**
- `↑↓`：浏览历史
- `Ctrl+A/E`：跳转行首/尾
- `Ctrl+U`：清除当前行

## 许可证

本项目遵循 MIT 许可证。使用 Nominatim 服务请遵守 [OSM 使用政策](https://operations.osmfoundation.org/policies/nominatim/)。

---

## 📚 相关文档

想了解详细的使用方法？请查看：

👉 **[完整使用指南](instruction.md)** - 从启动到退出的详细步骤、使用技巧和常见问题解答