FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Загрузка модели для spaCy
RUN python -m spacy download ru_core_news_sm

COPY . .

CMD ["python", "main.py"]
