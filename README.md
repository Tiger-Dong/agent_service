# Agent Service

基于 Ollama 的本地 AI 对话服务（使用 OpenAI Client）

## 功能特性

- 使用 OpenAI Client 连接本地 Ollama 服务
- 支持 Qwen3:8b 等模型
- 命令行交互界面
- 环境变量配置
- 错误处理机制
- 🗺️ **地理编码功能**：支持地址转经纬度查询（基于 OpenStreetMap）

## 环境要求

- Python 3.11+
- Ollama 服务

## 安装步骤

1. 克隆项目
```bash
git clone https://github.com/Tiger-Dong/agent_service.git
cd agent_service
```

2. 创建虚拟环境
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
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

### 每次运行前的步骤

1. 进入项目目录
```bash
cd /Users/DongZh/Desktop/tryOllama
```
2. 激活虚拟环境
```bash
source .venv/bin/activate
```
激活成功后，终端提示符前会显示 `(.venv)`

3. 运行程序
```bash
python main.py
```

4. 退出虚拟环境（程序结束后）
```bash
deactivate
```

### 快速运行（不持久激活）

如果不想激活虚拟环境，可以直接使用：
```bash
.venv/bin/python main.py
```

### 使用说明

**AI 对话模式：**
```bash
.venv/bin/python main.py
```
输入问题后回车即可与 AI 对话，输入 `exit` 或 `quit` 退出程序。

**地理编码模式：**
```bash
.venv/bin/python geocoding.py
```
输入任意地址，获取对应的经纬度坐标。
项目结构

```
agent_service/
├── main.py                  # AI 对话主程序（使用 OpenAI Client）
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
✅ 查技术特点

**AI 对话功能：**
- 使用 OpenAI 官方客户端库
- 兼容 OpenAI API 格式
- 轻松切换到其他 OpenAI 兼容的服务
- 使用 python-dotenv 管理环境变量

**地理编码功能：**
- 基于 OpenStreetMap Nominatim API
- 支持全球地址查询（中英文）
- 自动速率限制保护
- 返回详细地址信息和匹配度评分

## 许可证

本项目遵循 MIT 许可证。使用 Nominatim 服务请遵守 [OSM 使用政策](https://operations.osmfoundation.org/policies/nominatim/)。
📍 经度: 116.4074
📍 纬度: 39.9042
📝 完整地址: 北京市, 中国

请输入地址: Eiffel Tower
✅ 查询成功！
📍 配置说明
## 技术特点

- 使用 OpenAI 官方客户端库
- 兼容 OpenAI API 格式
- 轻松切换到其他 OpenAI 兼容的服务
- 使用 python-dotenv 管理环境变量
agent_service/
├── main.py           # 主程序
├── requirements.txt  # 依赖列表
├── README.md         # 项目说明
└── .gitignore       # Git 忽略文件
```
