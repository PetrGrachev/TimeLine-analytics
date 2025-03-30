FROM python:3.9-slim

WORKDIR /app

# Установим зависимости системы
RUN apt-get update && apt-get install -y gcc g++ libpq-dev && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY ../requirements-base.txt .
RUN pip install --no-cache-dir -r requirements-base.txt

COPY ../requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

# Копируем локальные модели и ресурсы
COPY models/feedbacks_analysis /app/models/feedbacks_analysis

# Копируем сам код
COPY . .

CMD ["python", "main.py"]
