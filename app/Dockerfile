FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Загрузка ресурсов
RUN python -m nltk.downloader stopwords
RUN python -m spacy download ru_core_news_sm
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')"
COPY . .

CMD ["python", "main.py"]
