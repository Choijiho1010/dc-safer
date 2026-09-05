FROM python:3.12-slim AS base
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

# 패키지 메타와 소스를 함께 넣는다. setuptools가 packages=["app"]를 해석하려면
# 설치 시점에 app/ 이 존재해야 한다.
COPY pyproject.toml ./
COPY app ./app
RUN pip install --no-cache-dir . "uvicorn[standard]"

EXPOSE 8000
HEALTHCHECK --interval=15s --timeout=3s --retries=5 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/healthz').status==200 else 1)"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
