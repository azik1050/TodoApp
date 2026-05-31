FROM python:3.14-slim

WORKDIR /app

COPY . .

RUN pip install uv
RUN uv sync

CMD ["uv", "run", "uvicorn", "src.application.app:create_app", "--host", "0.0.0.0", "--port", "8000"]