FROM astral/uv:python3.13-trixie-slim

WORKDIR /app

COPY . .

RUN uv sync --no-cache --locked

ENV OPENAI_API_KEY="sk-your-openai-api-key"
ENV OPENAI_BASE_URL="https://api.openai.com/v1"
ENV CLAUDE_HAIKU_MODEL="openai/gpt-4o-mini"
ENV CLAUDE_SONNET_MODEL="openai/gpt-4o"
ENV CLAUDE_OPUS_MODEL="openai/gpt-4o"
ENV HOST="127.0.0.1"
ENV PORT="8082"

EXPOSE $PORT

CMD ["uv", "run", "main.py"]
