FROM python:3.12-slim AS builder

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.12-slim

WORKDIR /app


RUN useradd --create-home --shell /bin/bash appuser

COPY --from=builder /opt/venv /opt/venv
COPY . .

RUN chown -R appuser:appuser /app

USER appuser
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000


HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]