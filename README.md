# Agent Service - AI 智能助手

> 基于 Ollama 本地大模型的智能对话助手，支持自然语言交互、地理查询和天气预报

## 📖 项目简介

这是一个使用 **Model-Based** 架构的 AI 智能助手，通过自然语言与用户交互，自动理解意图并调用相应工具完成任务。无需记忆命令，像和朋友聊天一样使用所有功能。

## ✨ 主要功能

- 🗺️ **地理查询** - 查询全球任意地点的经纬度坐标
- 🌤️ **天气预报** - 实时天气信息 + 智能穿衣建议
- 💬 **智能对话** - 多轮上下文理解，自然语言交互
- 🌐 **双语支持** - 中英文随时切换
- 🔧 **工具扩展** - 基于 MCP 协议，易于添加新功能

## 🚀 快速开始

### 环境要求

- Python 3.8+
- uv 包管理器
- Ollama 服务

### 安装运行

```bash
# 1. 克隆项目
git clone https://github.com/Tiger-Dong/agent_service.git
cd agent_service

# 2. 安装依赖（uv 会自动创建虚拟环境）
uv sync

# 3. 配置环境变量（可选）
cp .env.example .env

# 4. 下载并启动 Ollama 模型
ollama pull qwen3:8b
ollama serve

# 5. 启动助手
uv run python main.py
```

## ⚡ 马上运行

```bash
# 检查环境
ollama list                    # 确认 Ollama 已安装且运行中
python3 --version              # 确认 Python 版本 >= 3.8

# 检查/激活虚拟环境
source .venv/bin/activate      # 激活虚拟环境（如需要）
which python                   # 确认使用虚拟环境的 Python

# 启动程序
uv run python main.py          # uv 自动管理环境（无需手动激活虚拟环境）
# 或
python main.py                 # 已激活虚拟环境

# 结束程序
exit / quit / 退出             # 在程序中输入任一命令
# 或按 Ctrl+C                  # 强制退出
```

## 💡 使用示例

启动后，直接用自然语言与 AI 对话：

```bash
User: 北京今天天气怎么样？
Assistant: 
📍 查询地点: 北京市, 中国
🌡️ 当前温度: -5.2°C (冰点以下)
👔 出行建议: 寒冷，建议穿厚外套、毛衣、长裤
...

User: 切换到英文
Assistant: ✅ Language has been switched to English.

User: What's the weather in Tokyo?
Assistant: Tokyo weather today: 10°C, mainly clear...
```

**支持的查询示例：**
- 地理位置：`"北京天安门在哪里？"` / `"Where is the Eiffel Tower?"`
- 天气查询：`"明天去上海穿什么？"` / `"达拉斯冷还是休斯顿冷？"`
- 语言切换：`"切换到英文"` / `"switch to Chinese"`

## 📁 项目结构

```
tryOllama/
├── main.py              # 主程序（MCP 工具系统）
├── weather.py           # 天气查询模块
├── geocoding.py         # 地理编码模块
├── textD.py             # 多语言文本字典
├── test_all.py          # 完整测试套件
├── demo_weather.py      # 功能演示
├── pyproject.toml       # 项目配置
├── instruction.md       # 使用指南
└── docs/archive/        # 归档文档
```

## 🔧 技术特点

- **Model-Based 架构** - AI 自动理解意图，无需记忆命令
- **MCP 工具协议** - 标准化工具调用接口，易于扩展
- **双语支持** - 中英文界面和数据展示
- **免费 API** - 使用 Open-Meteo 和 OpenStreetMap，无需 API key

## 📝 配置说明

编辑 `.env` 文件可修改：
- `OLLAMA_BASE_URL` - Ollama 服务地址（默认：http://localhost:11434/v1）
- `MODEL_NAME` - 使用的模型（默认：qwen3:8b）

支持的模型：qwen3、llama3、deepseek 等所有 Ollama 兼容模型

## 📚 更多信息

- **完整使用指南**：[instruction.md](instruction.md) - 详细的使用步骤和技巧
- **测试功能**：运行 `uv run python test_all.py` 验证所有功能
- **功能演示**：运行 `uv run python demo_weather.py` 查看代码示例
- **精简记录**：[REFACTOR_SUMMARY.md](REFACTOR_SUMMARY.md) - 项目精简和重构详情

## ⚖️ 许可证

MIT License - 详见 [LICENSE](LICENSE)

使用 OpenStreetMap Nominatim 服务请遵守 [OSM 使用政策](https://operations.osmfoundation.org/policies/nominatim/)

---

**Star ⭐ 本项目** 如果你觉得有用！欢迎提 Issue 和 PR。