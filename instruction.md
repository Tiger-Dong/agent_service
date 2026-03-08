# 🚀 快速使用指南

Agent Service 智能助手 - 地理查询 + 天气预报 + AI 对话

---

## 前置准备

### 1. 确保 Ollama 服务运行中

```bash
# 检查 Ollama 是否运行
ollama list

# 如果没运行，启动 Ollama
ollama serve
```

### 2. 确保已下载模型

```bash
# 下载 Qwen 模型（如果还没有）
ollama pull qwen3:8b
```

---

## 启动程序

在项目目录下运行：

```bash
# 推荐方式：使用 uv（自动管理虚拟环境）
uv run python main.py

# 或者：手动激活虚拟环境
source .venv/bin/activate
python main.py
```

启动成功后会看到：

```
============================================================
🎯 智能助手 [Model-Based Mode]
💡 我可以理解你的自然语言指令！
============================================================

User:
```

---

## 功能使用

### 1. 查询地理位置

```
User: 北京天安门在哪里
User: Where is New York?
User: 东京的坐标
```

### 2. 查询天气 ⭐

```
User: 北京今天天气怎么样？
User: 明天去上海穿什么？
User: 达拉斯和休斯顿哪个更冷？
```

**AI 会自动：**
1. 查询地址坐标
2. 获取天气信息
3. 给出穿衣建议

**显示信息：**
- 📍 地点和坐标
- ☁️ 天气状况
- 🌡️ 温度区间和当前温度
- 👔 出行建议（穿衣+装备）
- 💧 湿度、💨 风速等

### 3. 切换语言

```
User: 切换到英文
User: switch to Chinese
```

### 4. 开关 AI Thinking 显示

```
User: 开启 thinking
User: 关闭 thinking
```

### 5. 退出程序

```
User: 退出
User: exit
User: bye
```

---

## 使用示例

```bash
$ uv run python main.py

User: 北京今天天气怎么样？

🔧 正在调用工具: geocode_address
🔧 正在调用工具: get_weather

Assistant：北京今天的天气：

📍 查询地点: 北京市, 中国
🗺️  坐标: (39.9042, 116.4074)
☁️  天气状况: 晴天 / Clear sky
🌡️  当天温度区间: -5.7°C ~ 1.4°C
🌡️  当前温度: -5.2°C (冰点以下)

👔 出行建议:
    • 寒冷，建议穿厚外套、毛衣、长裤

💧 湿度: 60%
💨 风速: 2.7 km/h

User: 退出
👋 Goodbye!
```

---

## 常见问题

### Q: 提示连接 Ollama 失败？
**A:** 确保 Ollama 服务在运行：`ollama serve`

### Q: 天气查询慢？
**A:** 需要调用两个 API（地理编码+天气），正常需要 2-5 秒

### Q: 想换模型？
**A:** 编辑 `.env` 文件，修改 `MODEL_NAME=其他模型名`

### Q: 清空对话历史？
**A:** 重启程序即可

---

## 快速测试

```bash
# 运行完整测试套件（包含所有测试项目）
uv run python test_all.py

# 运行功能演示
uv run python demo_weather.py
```

---

## 更多资源

- [README.md](README.md) - 项目详细文档
- [weather.py](weather.py) - 天气 API 模块
- [geocoding.py](geocoding.py) - 地理编码模块
- [docs/archive/](docs/archive/) - 归档的历史文档
