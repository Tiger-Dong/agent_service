# Agent Service

基于 Ollama 的本地 AI 对话服务（使用 OpenAI Client）

## 功能特性

- 🎯 **统一菜单系统**：一键启动，智能切换多种功能模式
- 🤖 **AI 对话模式**：使用 OpenAI Client 连接本地 Ollama 服务
- 🗺️ **地图查询模式**：支持地址转经纬度查询（基于 OpenStreetMap）
- ⚙️ **设置中心**：配置语言偏好和 AI 显示选项
  - 🌐 **完整多语言支持**（中文/English）
    - 所有界面文本实时切换
    - 支持中英文命令识别（如 "返回菜单" / "return menu"）
    - 无需重启，即时生效
  - 🤔 AI Thinking 显示开关（流式输出思考过程）
- 🔄 **模式切换**：在任意模式下输入 `返回菜单` 即可切换功能
- 💡 **智能命令识别**：支持数字、完整名称、简称等多种输入方式
- 支持 Qwen3:8b 等多种 AI 模型
- 命令行交互界面，操作简单直观
- 环境变量配置，灵活可定制
- 完善的错误处理机制
- 符合 DRY 原则的代码架构

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

3. 创建虚拟环境并安装依赖
```bash
uv venv
uv pip install -r requirements.txt
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

### 🚀 快速启动（推荐）

只需一条命令即可启动所有功能：

```bash
.venv/bin/python main.py
```

启动后会显示主菜单，你可以：
- 输入 `1` 或 `AI对话模式` 进入 AI 对话
- 输入 `2` 或 `地图查询模式` 进入地图查询
- 输入 `3` 或 `设置` 配置语言和显示选项
- 在任意模式中输入 `返回菜单` 切换到其他模式
- 随时输入 `exit`、`quit` 或 `退出` 结束程序

### 📋 主菜单示例

```
============================================================
🎯 多功能智能助手
============================================================
📋 可用模式：
  1️⃣  AI对话模式 - 与 Ollama AI 进行对话
  2️⃣  地图查询模式 - 查询地址的经纬度坐标
  3️⃣  设置 - 配置语言和显示选项
============================================================
💡 提示：在任意模式中输入 '返回菜单' 可返回主菜单
       输入 'exit' 或 'quit' 可退出程序

请选择模式（输入数字或模式名称）：
```

### 💬 模式选择方式

**方式 1：数字选择**
```bash
请选择模式：1         # 进入 AI 对话模式
请选择模式：2         # 进入地图查询模式
请选择模式：3         # 进入设置
```

**方式 2：完整名称**
```bash
请选择模式：AI对话模式
请选择模式：地图查询模式
请选择模式：设置
```

**方式 3：简称**
```bash
请选择模式：AI         # 进入 AI 对话模式
请选择模式：对话       # 进入 AI 对话模式
请选择模式：地图       # 进入地图查询模式
请选择模式：查询       # 进入地图查询模式
请选择模式：settings   # 进入设置（也可用：配置）
```

**💡 提示：** 输入不区分大小写，`AI`、`ai`、`Ai` 都可以识别

### 🔄 模式切换

在任意模式下，输入以下任一命令即可返回主菜单：
- `返回菜单`
- `菜单`
- `menu`
- `back`

### 🎮 完整使用流程

1. **启动程序**
```bash
cd /Users/DongZh/Desktop/tryOllama
.venv/bin/python main.py
```

2. **选择 AI 对话模式**
```
请选择模式：1
🤖 AI对话模式已启动
User：你好
Assistant：你好！有什么我可以帮助你的吗？

User：返回菜单
🔄 正在返回主菜单...
```

3. **切换到地图查询模式**
```
请选择模式：2
🌍 地图查询模式已启动
请输入地址：北京
✅ 查询成功！
📍 经度: 116.4074
📍 纬度: 39.9042

请输入地址：返回菜单
🔄 正在返回主菜单...
```

4. **进入设置修改配置**
```
请选择模式：3
⚙️  设置 / Settings
当前设置：
  1️⃣  语言 / Language: 中文
  2️⃣  显示 AI Thinking: 关闭

请选择要修改的设置：2
是否开启显示 AI thinking 过程？(y/n): y
✅ 已开启 AI thinking 显示

请选择要修改的设置：返回菜单
🔄 正在返回主菜单...
```

5. **退出程序**
```
请选择模式：exit
👋 感谢使用，再见！
```

### 📌 传统方式（仅供参考）

如果需要单独运行某个模式，仍可使用：

**仅 AI 对话：** （不推荐，建议使用主菜单）
```bash
# 已集成到主菜单，单独运行需要修改 main.py
```

**仅地理编码：** （不推荐，建议使用主菜单）
```bash
.venv/bin/python geocoding.py
```

### 🔧 虚拟环境管理（可选）

如果想激活虚拟环境后直接使用 `python`：

```bash
# 激活虚拟环境
source .venv/bin/activate

# 运行程序（激活后）
python main.py

# 退出虚拟环境
deactivate
```

## 项目结构

```
agent_service/
├── main.py                  # 主程序入口（统一菜单系统 + AI 对话）
├── geocoding.py             # 地理编码模块（OpenStreetMap）
├── geocoding_examples.py    # 地理编码使用示例
├── requirements.txt         # 依赖列表
├── .env                     # 环境变量配置（不上传到 Git）
├── .env.example             # 环境变量模板
├── README.md                # 项目说明
└── .gitignore              # Git 忽略文件
```
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
.venv/bin/python geocoding.py
```
输入地址，即可获得：
- 经度 (Longitude)
- 纬度 (Latitude)
- 完整显示地址
- 匹配度评分

**2. 批量查询示例：**
```bash
.venv/bin/python geocoding_examples.py
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

### ⚙️ 应用内设置

通过主菜单选择 `3. 设置` 可以配置以下选项：

#### 1. 🌐 语言设置 (Language)
- **中文**：所有界面显示为中文
- **English**：所有界面显示为英文
- **实时切换**：无需重启程序，立即生效
- **全面覆盖**：包括菜单、提示、错误信息等所有文本
- **命令支持**：中英文命令都能识别（如 "返回菜单" 和 "return menu"）

**语言切换效果对比：**

*中文界面：*
```
============================================================
🎯 多功能智能助手
============================================================
📋 可用模式：
  1️⃣  AI对话模式 - 与 Ollama AI 进行对话
  2️⃣  地图查询模式 - 查询地址的经纬度坐标
  3️⃣  设置 - 配置语言和显示选项
```

*English Interface:*
```
============================================================
🎯 Multi-functional AI Assistant
============================================================
📋 Available Modes:
  1️⃣  AI Chat Mode - Chat with Ollama AI
  2️⃣  Map Query Mode - Query address coordinates
  3️⃣  Settings - Configure language and display options
```

#### 2. 🤔 AI Thinking 显示
- **开启**：使用流式输出，逐字显示 AI 生成过程，可以看到 AI 的"思考"过程
- **关闭**：直接显示完整回答，响应更快
- 适合不同使用场景的需求

**使用示例：**
```bash
# 进入设置
请选择模式：3

# 修改语言为英文
请选择要修改的设置：1
请选择语言 / Select language (1/2): 2
✅ Switched to English

# 此时所有界面自动变为英文
Choose setting to modify: 2
Enable AI thinking display? (y/n): y
✅ AI thinking display enabled

# 返回菜单（英文命令）
Choose setting to modify: return menu
🔄 Returning to main menu...

# 主菜单现在是英文
Choose mode (number or name): 1
🤖 AI Chat Mode Started - Model: qwen3:8b
User: Hello
Assistant: Hello! How can I help you?
```

## 技术特点

**多语言架构：**
- 文本与逻辑完全分离
- 支持动态语言切换
- 易于扩展新语言
- 中英文命令智能识别

**AI 对话功能：**
- 使用 OpenAI 官方客户端库
- 兼容 OpenAI API 格式
- 轻松切换到其他 OpenAI 兼容的服务
- 使用 python-dotenv 管理环境变量
- 支持流式和非流式输出

**地理编码功能：**
- 基于 OpenStreetMap Nominatim API
- 支持全球地址查询（中英文）
- 自动速率限制保护
- 返回详细地址信息和匹配度评分

**代码架构：**
- 符合 DRY (Don't Repeat Yourself) 原则
- 模块化设计，易于维护和扩展
- 公共功能统一提取
- 配置集中管理

**包管理：**
- 使用 uv 替代传统 pip（速度提升 10-100 倍）
- 快速的依赖解析和安装
- 更好的依赖冲突解决

## 许可证

本项目遵循 MIT 许可证。使用 Nominatim 服务请遵守 [OSM 使用政策](https://operations.osmfoundation.org/policies/nominatim/)。

## 为什么选择 uv？

相比传统的 pip：
- ⚡ **速度快 10-100 倍**：Rust 编写，性能卓越
- 🔒 **可靠的依赖解析**：更准确的依赖冲突检测
- 💾 **全局缓存**：跨项目共享依赖，节省空间
- 🎯 **更好的用户体验**：清晰的进度显示和错误信息

更多信息：https://github.com/astral-sh/uv