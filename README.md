# Agent Service

基于 Ollama 的本地 AI 对话服务（使用 OpenAI Client）

## 功能特性

- 使用 OpenAI Client 连接本地 Ollama 服务
- 支持 Qwen3:8b 等模型
- 命令行交互界面
- 环境变量配置
- 错误处理机制

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

载入虚拟环境后 运行：.venv/bin/python main.py
即可启动程序

输入问题后回车即可与 AI 对话，输入 `exit` （使用 OpenAI Client）
├── requirements.txt  # 依赖列表
├── .env              # 环境变量配置（不上传到 Git）
├── .env.example      # 环境变量模板
├── README.md         # 项目说明
└── .gitignore       # Git 忽略文件
```

## 配置说明

`.env` 文件配置项：
- `OLLAMA_BASE_URL`: Ollama API 地址（默认：http://localhost:11434/v1）
- `OLLAMA_API_KEY`: API Key（Ollama 不验证，但必须提供）
- `MODEL_NAME`: 使用的模型名称（默认：qwen3:8b）

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
