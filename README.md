# OpenAI to Claude Proxy

这是一个轻量级的代理服务，提供将OpenAI兼容的API接口代理为Claude API兼容接口服务。

## 功能特性

- 🤖 **多提供商支持**: 后端可配置为Claude、OpenAI或其他AI模型提供商
- ⚡ **高性能**: 基于LiteLLM代理，性能优异
- 🐳 **Docker 支持**: 提供Dockerfile，便于容器化部署
- 🔧 **灵活配置**: 通过环境变量和YAML配置文件轻松定制模型映射

## 快速开始

### 先决条件

- Python 3.13 或更高版本
- [uv](https://docs.astral.sh/uv/) 包管理器（推荐）

### 安装与运行

1. 克隆仓库：
   ```bash
   git clone https://github.com/tuuzed/openai-to-claude.git
   cd openai-to-claude
   ```

2. 复制环境变量模板：
   ```bash
   cp .env.example .env
   ```

3. 编辑 `.env` 文件，配置您的API密钥和模型映射：
   ```env
   OPENAI_BASE_URL="https://api.openai.com/v1"
   OPENAI_API_KEY="sk-your-openai-api-key"

   CLAUDE_HAIKU_MODEL="openai/gpt-4o-mini"
   CLAUDE_SONNET_MODEL="openai/gpt-4o"
   CLAUDE_OPUS_MODEL="openai/gpt-4o"

   HOST="127.0.0.1"
   PORT="8082"
   ```

4. 安装依赖并启动服务：
   ```bash
   uv sync
   uv run main.py
   ```

5. 服务将在 `http://127.0.0.1:8082` 启动

### 使用 Docker

1. 构建镜像：
   ```bash
   docker build -t openai-to-claude .
   ```

2. 运行容器：
   ```bash
   docker run -p 8082:8082 --env-file .env openai-to-claude
   ```

## API 使用

服务启动后，您可以像使用OpenAI API一样使用它。通过指定不同的模型名称，请求会被路由到相应的后端模型：

```bash
# 调用Sonnet模型（默认配置映射到GPT-4o）
curl http://localhost:8082/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "model": "claude-sonnet",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'

# 调用Haiku模型（默认配置映射到GPT-4o-mini）
curl http://localhost:8082/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "model": "claude-haiku",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

支持的模型别名：
- `claude-haiku`
- `claude-sonnet` (默认)
- `claude-opus`

**注意**: 这些模型别名会根据 `config.yaml` 中的配置映射到实际的后端模型。

## 配置说明

### 环境变量

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `OPENAI_BASE_URL` | 后端API基础URL | `https://api.openai.com/v1` |
| `OPENAI_API_KEY` | 后端API密钥 | - |
| `CLAUDE_HAIKU_MODEL` | Haiku模型别名映射到的实际模型 | `openai/gpt-4o-mini` |
| `CLAUDE_SONNET_MODEL` | Sonnet模型别名映射到的实际模型 | `openai/gpt-4o` |
| `CLAUDE_OPUS_MODEL` | Opus模型别名映射到的实际模型 | `openai/gpt-4o` |
| `HOST` | 代理服务监听地址 | `127.0.0.1` |
| `PORT` | 代理服务监听端口 | `8082` |

**模型格式说明**:
- OpenAI模型: `openai/gpt-4o`, `openai/gpt-4o-mini`
- Claude模型: `anthropic/claude-3-5-sonnet-20241022`, `anthropic/claude-3-haiku-20240307`
- 其他提供商: 查看 [LiteLLM支持的模型列表](https://docs.litellm.ai/docs/providers)

### 中间件功能

项目包含自定义中间件 `claude_middleware.py`，它会在请求发送到后端之前，将客户端请求中的模型名称标准化为配置文件中定义的模型别名。例如：
- 客户端请求包含 "haiku" 的模型名 → 映射为 `claude-haiku`
- 客户端请求包含 "sonnet" 的模型名 → 映射为 `claude-sonnet`
- 客户端请求包含 "opus" 的模型名 → 映射为 `claude-opus`

这样可以提供更灵活的模型调用方式，同时保持配置的一致性。

## 项目结构

```
openai-to-claude/
├── main.py              # 主入口文件
├── config.yaml          # LiteLLM配置文件
├── claude_middleware.py # 自定义中间件
├── Dockerfile           # Docker构建文件
├── pyproject.toml       # 项目依赖配置
├── uv.lock             # 依赖锁定文件
├── .env.example        # 环境变量模板
└── README.md           # 本文档
```

## 依赖

- [LiteLLM](https://litellm.ai/) >= 1.80.12
- [python-dotenv](https://pypi.org/project/python-dotenv/) >= 1.2.1

## 许可证

本项目采用 MIT 许可证。

## 注意事项

- 请确保在生产环境中安全地管理您的API密钥
- 默认配置示例使用OpenAI的GPT模型作为后端，您可以修改 `.env` 文件中的 `CLAUDE_*_MODEL` 变量来配置真正的Claude API或其他模型提供商
- 要使用真正的Claude API，将模型配置改为类似 `anthropic/claude-3-5-sonnet-20241022` 格式，并设置相应的Anthropic API密钥
- 服务默认只监听本地地址，如需外部访问，请修改 `HOST` 环境变量为 `0.0.0.0`