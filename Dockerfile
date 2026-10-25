FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY tests/ ./tests/
COPY paper/ ./paper/
CMD ["python", "-m", "unittest", "discover", "-s", "tests", "-v"]
