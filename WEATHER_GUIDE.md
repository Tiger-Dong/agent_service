# 🌤️ 天气功能使用指南

## 新增功能概述

现在你可以通过自然语言询问任何地方的天气，并获得智能穿衣建议！

## 🚀 快速开始

### 1. 直接询问天气

只需用自然语言提问，AI 会自动：
1. 识别地点并查询经纬度
2. 根据坐标查询天气
3. 提供穿衣建议

### 2. 使用示例

#### 示例 1：基础天气查询

```bash
User：北京今天天气怎么样？

🔧 正在调用工具: geocode_address
📍 查询地址: 北京

🔧 正在调用工具: get_weather
🌤️  查询天气: (39.9042, 116.4074)

Assistant：北京今天的天气如下：

📍 当前天气：
- 🌡️  温度：-2°C
- 🤔 体感温度：-5°C
- ☁️  天气：晴天 / Clear sky
- 💧 湿度：45%
- 💨 风速：8 km/h

👔 穿衣建议：
寒冷，建议穿厚外套、毛衣、长裤 | Cold - thick coat, sweater, long pants

📅 未来3天预报：
2026-01-14: -3°C ~ 5°C (晴天)
2026-01-15: -1°C ~ 6°C (局部多云)
2026-01-16: 0°C ~ 7°C (基本晴朗)
```

#### 示例 2：询问穿衣建议

```bash
User：明天去纽约应该穿什么衣服？

🔧 正在调用工具: geocode_address
📍 查询地址: 纽约

🔧 正在调用工具: get_weather

Assistant：纽约明天的天气：
- 温度：12°C ~ 18°C
- 天气：局部多云 / Partly cloudy
- 湿度：60%

👔 穿衣建议：
较冷，建议穿夹克、卫衣、长裤 | Cool - jacket, hoodie, long pants
```

#### 示例 3：对比多个城市

```bash
User：达拉斯和休斯顿明天哪个更冷？

🔧 正在调用工具: geocode_address (达拉斯)
🔧 正在调用工具: get_weather

Assistant：达拉斯明天：15°C ~ 22°C

🔧 正在调用工具: geocode_address (休斯顿)
🔧 正在调用工具: get_weather

Assistant：休斯顿明天：18°C ~ 25°C

总结：达拉斯更冷一些。达拉斯建议穿长袖衬衫和薄外套，休斯顿可以穿短袖。
```

#### 示例 4：英文查询

```bash
User：What should I wear in Tokyo tomorrow?

🔧 Calling tool: geocode_address
📍 Query address: Tokyo

🔧 Calling tool: get_weather
🌤️  Query weather: (35.6895, 139.6917)

Assistant：Tokyo tomorrow's weather:
- Temperature: 8°C ~ 15°C
- Weather: Mainly clear
- Humidity: 55%

👔 Clothing Advice:
Cool - jacket, hoodie, long pants
```

## 🎯 支持的查询方式

AI 能理解各种自然语言表达：

### 查询天气
- "北京今天天气怎么样？"
- "What's the weather in New York?"
- "上海明天会下雨吗？"
- "Tell me about Tokyo's weather"

### 询问穿衣建议
- "明天去纽约应该穿什么？"
- "去吉林需要穿羽绒服吗？"
- "What should I wear in London tomorrow?"
- "达拉斯冷还是休斯顿冷？"

### 对比多地天气
- "北京和上海哪个更暖和？"
- "Compare weather in Dallas and Houston"
- "纽约和伦敦明天温度差多少？"

## 🌡️ 温度对应的穿衣建议

AI 会根据温度自动给出建议：

| 温度范围 | 穿衣建议 |
|---------|---------|
| < -10°C | 羽绒服、厚毛衣、保暖内衣 |
| -10°C ~ 0°C | 厚外套、毛衣、长裤 |
| 0°C ~ 10°C | 夹克、卫衣、长裤 |
| 10°C ~ 20°C | 长袖衬衫、薄外套 |
| 20°C ~ 28°C | 短袖、长裤 |
| > 28°C | 短袖、短裤 |

## ☁️ 特殊天气提醒

AI 还会根据天气状况给出额外建议：

- **有雨** → 记得带伞
- **有雪** → 注意保暖和防滑
- **雷暴** → 尽量避免外出

## 📊 天气数据来源

- **API**: Open-Meteo（免费、无需API key）
- **数据**: 全球天气预报
- **更新**: 实时数据
- **范围**: 当前天气 + 未来7天预报

## 🔧 工具链串联

当你问"某地天气"时，AI 自动执行：

```
用户提问
  ↓
1. geocode_address(地点)
  ↓ 返回经纬度
2. get_weather(lat, lon)
  ↓ 返回天气数据
3. 分析温度和天气
  ↓
4. 给出穿衣建议
```

## 💡 使用技巧

### 1. 无需记忆命令
像和朋友聊天一样问就行：
- ✅ "明天去上海穿什么？"
- ✅ "北京冷吗？"
- ✅ "东京会下雨吗？"

### 2. 支持中英文混用
- ✅ "New York 今天天气如何？"
- ✅ "What's the weather in 北京?"

### 3. 连续对话
AI 会记住上下文：
```bash
User：查一下巴黎的天气
Assistant：[显示巴黎天气]

User：那里冷吗？
Assistant：[AI 知道"那里"指巴黎]
```

### 4. 模糊表达也能懂
- "那边天气怎么样？"（AI 会问你指哪里）
- "会冷吗？"（如果前面提到了地点，AI 会理解）

## 🧪 测试功能

### 测试独立天气模块

```bash
# 运行天气模块测试
uv run python weather.py

# 或运行示例代码
uv run python weather_examples.py
```

### 在主程序中测试

```bash
uv run python main.py

# 然后尝试这些问题：
User：北京今天天气怎么样？
User：明天去纽约穿什么？
User：达拉斯和休斯顿哪个更冷？
```

## ❓ 常见问题

### Q: 为什么查询速度有点慢？

A: 需要串联调用两个 API（地理编码 + 天气查询），正常情况下 2-5 秒。

### Q: 支持哪些地区？

A: 全球所有地区！只要能查到坐标的地方都能查天气。

### Q: 天气数据准确吗？

A: 使用 Open-Meteo API，数据来自官方气象数据源，准确度很高。

### Q: 穿衣建议会考虑个人体感吗？

A: 目前是通用建议。未来可以添加个人偏好设置。

### Q: 可以查询历史天气吗？

A: 目前只支持当前和未来7天的预报。

## 🎉 开始使用

现在就试试新功能吧！

```bash
uv run python main.py
```

然后问 AI：
- "今天天气怎么样？"
- "明天该穿什么？"
- "帮我看看纽约的天气"

---

**提示**：如有任何问题，请查看 [README.md](README.md) 或 [instruction.md](instruction.md)。
