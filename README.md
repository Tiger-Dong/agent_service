# Agent Service

基于 Ollama 的本地 AI 对话服务

## 功能特性

- 使用本地部署的 Qwen3:8b 模型
- 命令行交互界面
- 非流式输出模式

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

4. 安装并启动 Ollama
```bash
# 下载模型
ollama pull qwen3:8b

# 启动服务
ollama serve
```

## 使用方法

```bash
source .venv/bin/activate
python main.py
```

输入问题后回车即可与 AI 对话，输入 `exit` 或 `quit` 退出程序。

## 项目结构

```
agent_service/
├── main.py           # 主程序
├── requirements.txt  # 依赖列表
├── README.md         # 项目说明
└── .gitignore       # Git 忽略文件
```
