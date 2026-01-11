# 🚀 完整使用流程

本文档提供详细的使用指南，帮助你快速上手 Agent Service 智能助手。

## 第一步：启动虚拟环境

在项目目录下，有两种方式启动程序：

**方式一：使用 uv 运行（推荐）**
```bash
# uv 会自动管理虚拟环境
uv run python main.py
```

**方式二：激活虚拟环境后运行**
```bash
# 激活虚拟环境
source .venv/bin/activate

# 运行程序
python main.py
```

## 第二步：开始使用

程序启动后，你会看到欢迎界面：

```
============================================================
🎯 智能助手 [Model-Based Mode]
💡 我可以理解你的自然语言指令！
============================================================

User:
```

现在你可以直接用自然语言与 AI 交流了！

## 第三步：进行对话和操作

### 📍 查询地理位置

直接用自然语言询问：

```bash
User: 帮我查一下北京天安门在哪里

🔧 正在调用工具: geocode_address
📍 查询地址: 北京天安门

Assistant：北京天安门的坐标如下：
- 经度：116.3974°
- 纬度：39.9075°
- 完整地址：天安门, 北京市, 中国
```

其他可以说的话：
- "巴黎在哪里？"
- "Where is New York?"
- "东京的坐标"
- "查一下上海埃菲尔铁塔"

### 🌐 切换语言

随时可以切换界面语言：

```bash
User: 切换到英文

🔧 正在调用工具: switch_language
Assistant：✅ Language has been switched to English.

# 此时所有界面文本都变成英文了
User: switch to Chinese

🔧 Calling tool: switch_language
Assistant：✅ 已切换到中文。
```

### 🤔 控制思考过程显示

想看 AI 怎么思考的？

```bash
User: 开启 thinking

🔧 正在调用工具: toggle_thinking
Assistant：✅ 已开启 AI thinking 显示功能。

User: 什么是人工智能？

🤔 AI 正在思考...
人（逐字）工（逐字）智（逐字）能...
[可以看到文字一个个出现]

# 不想看了？
User: 关闭 thinking

🔧 正在调用工具: toggle_thinking
Assistant：✅ 已关闭 AI thinking 显示功能。
```

### 💬 多轮对话

AI 会记住对话历史，可以连续提问：

```bash
User: 查一下巴黎的坐标
Assistant：巴黎的坐标是：经度 2.3522°，纬度 48.8566°

User: 那里有什么著名景点？
Assistant：巴黎有很多著名景点，包括埃菲尔铁塔、卢浮宫...

User: 埃菲尔铁塔具体在哪？
Assistant：让我查一下...
[AI 自动调用 geocode 工具查询埃菲尔铁塔坐标]
```

AI 理解你在说"埃菲尔铁塔"是因为前面聊到了巴黎！

## 第四步：退出程序

想退出时，随时用自然语言说：

```bash
User: 退出

🔧 正在调用工具: navigate
Assistant：感谢使用！再见！
👋 Goodbye!

[程序优雅退出]
```

其他退出方式：
- "exit"
- "bye"
- "goodbye"
- "我要走了"
- "quit"

**如果之前激活了虚拟环境，记得退出：**
```bash
deactivate
```

## 💡 使用技巧

### 1. 不需要记忆任何命令
- 像和朋友聊天一样说话即可
- AI 会自动理解你的意图

### 2. 表达方式灵活
- "帮我查一下北京在哪里" ✅
- "北京的坐标是多少" ✅
- "Where is Beijing" ✅
- "我想知道北京的位置" ✅

都能正确理解！

### 3. 中英文混用也可以
- "查一下 New York 的坐标" ✅
- "switch to 中文" ✅

### 4. 模糊表达也能懂
- "我想看你怎么思考的" → AI 理解为"开启 thinking"
- "换个语言" → AI 会询问你要换成什么语言
- "找个地方" → AI 会问你要找哪个地方

### 5. 支持连续对话
- AI 会记住对话历史
- 可以接着上一个话题继续聊

## ❓ 常见问题

### Q: 启动后提示找不到 Ollama 服务？

A: 确保 Ollama 服务已启动：
```bash
ollama serve
```

### Q: 模型响应很慢？

A: 首次使用会加载模型，需要等待。后续使用会快很多。

### Q: 想更换其他模型？

A: 编辑 `.env` 文件，修改 `MODEL_NAME` 参数：
```bash
MODEL_NAME=llama2:7b  # 更换为其他模型
```

### Q: 地理查询结果不准确？

A: 尝试更详细的地址描述，如：
- "北京天安门" 比 "天安门" 更准确
- "Paris, France" 比 "Paris" 更准确

### Q: 如何清空对话历史？

A: 重新启动程序即可清空历史记录。

## 🎯 完整使用示例

以下是一个完整的使用场景：

```bash
# 1. 启动程序
$ uv run python main.py

============================================================
🎯 智能助手 [Model-Based Mode]
💡 我可以理解你的自然语言指令！
============================================================

# 2. 开始对话
User: 你好，我想查一些城市的坐标

Assistant：你好！我可以帮你查询任何城市或地址的坐标。请告诉我你想查询哪个城市？

# 3. 查询地理位置
User: 北京

🔧 正在调用工具: geocode_address
📍 查询地址: 北京

Assistant：北京的坐标信息如下：
- 经度：116.4074°
- 纬度：39.9042°
- 完整地址：北京市, 中国

# 4. 继续查询
User: 那上海和广州呢？

🔧 正在调用工具: geocode_address
📍 查询地址: 上海

Assistant：上海的坐标是：经度 121.4737°，纬度 31.2304°

🔧 正在调用工具: geocode_address
📍 查询地址: 广州

Assistant：广州的坐标是：经度 113.2644°，纬度 23.1291°

# 5. 切换语言
User: 切换到英文

🔧 正在调用工具: switch_language
Assistant：✅ Language has been switched to English.

# 6. 用英文查询
User: What about Tokyo?

🔧 Calling tool: geocode_address
📍 Query address: Tokyo

Assistant：Here are the coordinates for Tokyo:
- Longitude: 139.6917°
- Latitude: 35.6895°
- Full address: Tokyo, Japan

# 7. 退出程序
User: That's all, bye!

🔧 Calling tool: navigate
Assistant：Thank you for using! Goodbye!
👋 Goodbye!

[程序退出]

# 8. 退出虚拟环境（如果之前激活了）
$ deactivate
```

---

现在你已经掌握了完整的使用流程！开始享受智能助手带来的便利吧！ 🎉

## 📚 更多资源

- [README.md](README.md) - 项目主文档
- [geocoding.py](geocoding.py) - 地理编码模块
- [main.py](main.py) - 主程序源码
