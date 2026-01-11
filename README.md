# Agent Service - Model-Based AI Assistant

基于 Ollama 的智能对话助手（Model-Based 架构 + MCP 工具调用）

## 功能特性

### 🎯 Model-Based 智能架构
- **自然语言理解**：无需记忆命令，用人类自然语言交流即可
- **意图自动识别**：AI 理解你的需求并自动调用相应工具
- **零学习成本**：像和朋友聊天一样使用所有功能

### 🔧 MCP 工具调用系统
基于 Model Context Protocol (MCP) 实现的 4 大智能工具：

1. **geocode_address** - 地理编码工具
   - 📍 查询全球任意地址的经纬度坐标
   - 🌍 支持中英文地址（如："北京天安门"、"Eiffel Tower"）
   - 📝 返回完整地址信息和匹配度评分

2. **switch_language** - 语言切换工具
   - 🌐 动态切换界面语言（中文/English）
   - 🔄 所有文本实时切换，无需重启
   - 💬 中英文命令都能识别

3. **toggle_thinking** - AI 思考过程开关
   - 🤔 控制是否显示 AI 逐字思考过程
   - 🌊 支持流式输出，观察 AI 生成过程
   - ⚡ 关闭后直接显示结果，响应更快

4. **navigate** - 导航控制工具
   - 🚪 退出程序或返回菜单
   - 🔄 智能识别退出意图

### 💬 核心特性
- 🤖 使用 OpenAI Client 连接本地 Ollama 服务
- 📝 完整的对话历史记忆，支持多轮上下文理解
- 🎨 友好的命令行交互界面
- 🛡️ 完善的错误处理机制
- 🏗️ 符合 DRY 原则的代码架构
- 🔌 支持 Qwen3:8b 等多种 AI 模型
- ⚙️ 环境变量配置，灵活可定制

## 环境要求

- Python 3.8+
- uv（超快的 Python 包管理器）
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

#### 2. 切换语言

```bash
User：切换到英文

🔧 正在调用工具: switch_language
Assistant：✅ Language has been switched to English.
```

**其他表达方式：** "我想用英文" / "change language to English" / "切换语言"

#### 3. 控制思考过程显示

```bash
User：开启 thinking

🔧 正在调用工具: toggle_thinking
Assistant：✅ 已开启 AI thinking 显示功能。
从现在开始，你可以看到我逐字生成回答的过程。
```

**其他表达方式：** "我想看思考过程" / "enable thinking" / "关闭 thinking" / "disable thinking"

#### 4. 退出程序

**示例：** "退出" / "exit" / "bye" / "goodbye"

### 🎨 多轮对话示例

```bash
User：帮我查一下北京的坐标
Assistant：北京的坐标信息如下：经度 116.4074°，纬度 39.9042°

User：那上海呢？
Assistant：上海的坐标信息如下：经度 121.4737°，纬度 31.2304°

User：切换到英文
Assistant：✅ Successfully switched to English.

User：What about Tokyo?
Assistant：Here are the coordinates for Tokyo: 139.6917°E, 35.6895°N

User：exit
Assistant：👋 Goodbye!
```

## 项目结构

```
agent_service/
├── main.py                  # 主程序（Model-Based 架构 + MCP 工具系统）
│   ├── SYSTEM_PROMPT       # AI 意图理解的系统提示词（中英双语）
│   ├── TOOLS               # 4 个 MCP 工具定义（geocode/language/thinking/navigate）
│   ├── execute_tool()      # 统一工具执行函数
│   ├── ask_qwen()          # AI 调用函数（支持工具调用）
│   └── ai_chat_mode()      # Model-Based 对话模式
├── textD.py                 # 多语言文本字典（keyword→language 结构）
├── geocoding.py             # 地理编码模块（OpenStreetMap Nominatim）
├── geocoding_examples.py    # 地理编码使用示例
├── requirements.txt         # Python 依赖列表
├── .env                     # 环境变量配置（不上传到 Git）
├── .env.example             # 环境变量模板
├── README.md                # 项目说明文档
└── .gitignore              # Git 忽略配置
```

## 🔧 MCP 工具调用技术详解

### 什么是 MCP？

Model Context Protocol (MCP) 是一种让 AI 模型能够调用外部工具的标准协议。本项目实现了基于 **OpenAI Function Calling** 标准的 MCP 工具系统。

### 架构优势

#### Model-Based vs Rule-Based

| 特性 | Rule-Based（传统） | Model-Based（本项目） |
|------|-------------------|----------------------|
| 命令识别 | 固定关键词匹配 | 自然语言理解 |
| 用户体验 | 需要记忆命令 | 像聊天一样交互 |
| 扩展性 | 需要添加规则 | AI 自动适应 |
| 灵活性 | 输入格式严格 | 接受各种表达 |
| 维护成本 | 高（规则爆炸） | 低（统一处理） |

**示例对比：**
```bash
# Rule-Based 传统方式
1. 输入 "1" 选择地图模式
2. 等待提示 "请输入地址"
3. 输入地址
4. 获得结果

# Model-Based 现代方式
直接说："帮我查一下北京天安门在哪里" → 完成✅
```

### 4 大智能工具详解

#### 1. 🌍 geocode_address - 地理编码工具

**功能：** 将地址转换为经纬度坐标

**触发方式（自然语言）：**
- "帮我查一下[地址]在哪里"
- "[地址]的坐标是多少"
- "我想知道[地址]的位置"
- "Where is [location]?"
- "Find [address] for me"

**输入：** 地址字符串（中英文均可）

**输出：** JSON 格式
```json
{
  "success": true,
  "longitude": 2.2945,
  "latitude": 48.8580,
  "display_name": "Tour Eiffel, Paris, France",
  "importance": 0.85
}
```

**应用场景：**
- 📍 地理位置查询
- 🗺️ 导航路线规划
- 📊 地理数据分析
- 🌐 多地址批量查询

#### 2. 🌐 switch_language - 语言切换工具

**功能：** 动态切换界面语言

**触发方式（自然语言）：**
- "切换到英文"
- "我想用中文"
- "Switch to English"
- "Change language"
- "换个语言"

**输入：** 目标语言代码（cn/en）

**输出：** JSON 格式
```json
{
  "success": true,
  "old_language": "cn",
  "new_language": "en",
  "message": "✅ Switched to English"
}
```

**特点：**
- 🔄 实时切换，无需重启
- 🌍 支持 50+ 界面文本
- 💬 中英文命令都识别
- 📝 所有文本来自 textD.py

#### 3. 🤔 toggle_thinking - AI 思考过程开关

**功能：** 控制是否显示 AI 逐字生成过程

**触发方式（自然语言）：**
- "开启 thinking"
- "我想看思考过程"
- "Enable thinking"
- "Show me how you think"
- "关闭 thinking" / "Disable thinking"

**输入：** 布尔值（true/false）

**输出：** JSON 格式
```json
{
  "success": true,
  "thinking_enabled": true,
  "message": "✅ AI Thinking On"
}
```

**效果对比：**
```bash
# Thinking 关闭（默认）
User：什么是AI？
Assistant：AI 是人工智能的缩写...[完整回答]

# Thinking 开启
User：什么是AI？
🤔 AI 正在思考...
AI（逐字出现） 是（逐字） 人工（逐字） 智能（逐字）...
```

#### 4. 🚪 navigate - 导航控制工具

**功能：** 控制程序流程（退出/返回）

**触发方式（自然语言）：**
- "退出" / "exit"
- "我要走了" / "bye"
- "quit" / "goodbye"
- "返回菜单" / "return menu"

**输入：** 动作类型（exit/menu）

**输出：** JSON 格式
```json
{
  "success": true,
  "action": "exit",
  "message": "Navigation action recorded"
}
```

**特点：**
- 🔄 优雅退出，保存状态
- 💬 多种表达方式识别
- 🌐 中英文都支持

### 工作流程

```
用户输入自然语言
       ↓
   SYSTEM_PROMPT 引导
       ↓
  AI 理解意图
       ↓
   选择合适工具
       ↓
  execute_tool() 执行
       ↓
   返回 JSON 结果
       ↓
  AI 解析并友好呈现
       ↓
   用户看到结果
```

### 扩展新工具

项目架构支持轻松添加新工具，只需 3 步：

#### 步骤 1：定义工具 Schema

在 `main.py` 中添加：
```python
NEW_TOOL = {
    "type": "function",
    "function": {
        "name": "tool_name",
        "description": "工具功能描述",
        "parameters": {
            "type": "object",
            "properties": {
                "param_name": {
                    "type": "string",
                    "description": "参数说明"
                }
            },
            "required": ["param_name"]
        }
    }
}

# 添加到 TOOLS 列表
TOOLS = [GEOCODING_TOOL, LANGUAGE_TOOL, THINKING_TOOL, NAVIGATE_TOOL, NEW_TOOL]
```

#### 步骤 2：实现工具逻辑

在 `execute_tool()` 函数中添加：
```python
def execute_tool(tool_name: str, arguments: dict) -> str:
    # ... 现有工具代码 ...
    
    elif tool_name == "tool_name":
        # 实现你的工具逻辑
        result = do_something(arguments)
        return json.dumps({
            "success": True,
            "result": result
        }, ensure_ascii=False)
```

#### 步骤 3：更新系统提示词

在 `SYSTEM_PROMPT` 中告诉 AI 何时使用新工具：
```python
SYSTEM_PROMPT = {
    "cn": """...
    - 当用户想[使用场景]时，使用 tool_name 工具
    ..."""
}
```

**完成！** AI 会自动学习何时调用新工具。

### 技术实现细节

**基于 OpenAI Function Calling：**
```python
response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=messages,
    tools=TOOLS,  # 传入工具定义
    temperature=0.7
)

# AI 决定是否调用工具
if response.choices[0].message.tool_calls:
    # 执行工具调用
    for tool_call in response.choices[0].message.tool_calls:
        result = execute_tool(
            tool_call.function.name,
            json.loads(tool_call.function.arguments)
        )
```

**优势：**
- ✅ 遵循 OpenAI 标准
- ✅ 兼容多种模型（Qwen、Llama 等）
- ✅ 支持工具链（Tool Chain）
- ✅ 易于调试和测试

## 地理编码功能 🗺️

### 功能说明

使用 OpenStreetMap Nominatim API 进行地理编码，将地址转换为经纬度坐标。

### 支持的地址格式

- **城市名**：`Beijing, China` / `东京`
- **地标**：`Eiffel Tower, Paris` / `北京天安门`
- **详细地址**：`1600 Amphitheatre Parkway, Mountain View, CA`
- **中英文均可**：支持全球范围内的地址查询

### 运行方式

**1. 交互式查询：**
```bash
uv run python geocoding.py
```
输入地址，即可获得：
- 经度 (Longitude)
- 纬度 (Latitude)
- 完整显示地址
- 匹配度评分

**2. 批量查询示例：**
```bash
uv run python geocoding_examples.py
```
运行预设的示例，展示：
- 基础用法
- 详细信息获取
- 批量处理示例

**3. 在代码中使用：**
```python
from geocoding import NominatimGeocoder

geocoder = NominatimGeocoder()

# 简单查询
coords = geocoder.get_coordinates("北京")
if coords:
    lat, lon = coords
    print(f"纬度: {lat}, 经度: {lon}")

# 详细查询
result = geocoder.geocode("Tokyo, Japan")
if result:
    print(f"经度: {result['longitude']}")
    print(f"纬度: {result['latitude']}")
    print(f"地址: {result['display_name']}")
```

### 使用注意事项

⚠️ **重要提示：**
- Nominatim 要求请求间隔**至少 1 秒**（已自动处理）
- 请勿用于商业大规模批量查询
- 遵守 [Nominatim 使用政策](https://operations.osmfoundation.org/policies/nominatim/)
- 建议为高频使用场景自建 Nominatim 服务器

### 查询示例

```bash
请输入地址: Beijing, China
✅ 查询成功！
📍 经度: 116.4074
📍 纬度: 39.9042
📝 完整地址: 北京市, 中国

请输入地址: Eiffel Tower
✅ 查询成功！
📍 经度: 2.2945
📍 纬度: 48.8584
📝 完整地址: Tour Eiffel, Paris, France
```

## 配置说明

### 环境变量配置

`.env` 文件配置项：
- `OLLAMA_BASE_URL`: Ollama API 地址（默认：http://localhost:11434/v1）
- `OLLAMA_API_KEY`: API Key（Ollama 不验证，但必须提供）
- `MODEL_NAME`: 使用的模型名称（默认：qwen3:8b）

## 技术特点

### 🏗️ Model-Based 智能架构
- **🎯 自然语言理解**：基于 SYSTEM_PROMPT 的意图识别系统
- **🤖 零规则匹配**：完全移除硬编码关键词，AI 自主判断
- **🔄 上下文感知**：完整对话历史，支持多轮理解
- **📊 结构化输出**：工具返回 JSON，AI 自动格式化呈现

### 🔧 MCP 工具调用系统
- **⚡ OpenAI Function Calling 标准**：兼容多种模型
- **4 大智能工具**：geocode / language / thinking / navigate
- **🔌 即插即用**：3 步添加新工具，AI 自动适配
- **💡 智能派发**：AI 自主选择合适工具，无需人工指定
- **🔗 工具链支持**：可串联多个工具完成复杂任务

### 🌐 多语言架构
- **📁 textD.py**：文本字典独立文件，逻辑与展示完全分离
- **🔄 优化结构**：keyword→language 双层结构，易于维护
- **🌍 动态切换**：实时语言切换，无需重启程序
- **🎯 智能识别**：中英文命令都能理解
- **📝 50+ 文本条目**：覆盖所有界面元素

### 🤖 AI 对话功能
- **OpenAI 官方客户端**：使用标准 SDK
- **⚡ API 兼容**：支持 OpenAI / Ollama / 其他兼容服务
- **🌊 流式输出**：支持 streaming 模式观察思考过程
- **📝 对话历史**：完整上下文记忆，支持多轮交互
- **🔐 环境变量**：使用 python-dotenv 安全管理配置

### 🗺️ 地理编码功能
- **OpenStreetMap Nominatim API**：免费开源地理服务
- **🌍 全球覆盖**：支持世界各地地址查询
- **🔤 多语言**：中英文地址都能识别
- **⏱️ 速率保护**：自动限速，遵守 OSM 使用政策
- **📊 详细信息**：返回坐标、完整地址、匹配度评分

### 💻 代码架构
- **DRY 原则**：无重复代码，统一处理逻辑
- **模块化设计**：功能独立，易于维护和扩展
- **📦 公共函数**：t() 函数统一文本获取，execute_tool() 统一工具执行
- **⚙️ 集中配置**：SETTINGS 全局配置，.env 环境变量
- **📏 代码精简**：从 530 行优化到 420 行（减少 21%）

### ⚡ 包管理
- **uv 超快速度**：Rust 编写，比 pip 快 10-100 倍
- **🔒 可靠解析**：更准确的依赖冲突检测
- **💾 全局缓存**：跨项目共享依赖，节省空间
- **🎯 更好体验**：清晰的进度显示和错误信息

## 许可证

本项目遵循 MIT 许可证。使用 Nominatim 服务请遵守 [OSM 使用政策](https://operations.osmfoundation.org/policies/nominatim/)。

## 为什么选择 uv？

相比传统的 pip：
- ⚡ **速度快 10-100 倍**：Rust 编写，性能卓越
- 🔒 **可靠的依赖解析**：更准确的依赖冲突检测
- 💾 **全局缓存**：跨项目共享依赖，节省空间
- 🎯 **更好的用户体验**：清晰的进度显示和错误信息

更多信息：https://github.com/astral-sh/uv

---

## � 相关文档

想了解详细的使用方法？请查看：

👉 **[完整使用指南](instruction.md)** - 从启动到退出的详细步骤、使用技巧和常见问题解答