from keybert import KeyBERT
import logging
import nltk
from nltk.corpus import stopwords

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузим список, если не установлен
try:
    russian_stopwords = stopwords.words("russian")
except LookupError:
    nltk.download("stopwords")
    russian_stopwords = stopwords.words("russian")

# Загружаем многоязычную модель от Sentence Transformers (поддерживает русский)
kw_model = KeyBERT(model="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

def get_keywords(feedback_texts, top_n=10):
    try:
        combined_text = " ".join(feedback_texts)

        logger.info(f"💬 Объединённый текст отзывов: {combined_text[:200]}...")

        keywords = kw_model.extract_keywords(
            combined_text,
            keyphrase_ngram_range=(1, 3),
            stop_words=russian_stopwords,
            top_n=top_n,
            use_maxsum=True,
            nr_candidates=20
        )

        logger.info(f"🔍 Найдено ключевых фраз: {keywords}")

        # Условная классификация — первые top_n//2 как positive, остальные как negative
        positive_keywords = [{"phrase": phrase, "score": score} for phrase, score in keywords[:top_n//2]]
        negative_keywords = [{"phrase": phrase, "score": score} for phrase, score in keywords[top_n//2:]]

        return {
            "positive_keywords": positive_keywords,
            "negative_keywords": negative_keywords
        }

    except Exception as e:
        logger.exception("❌ Ошибка при извлечении ключевых фраз:")
        return {"positive_keywords": [], "negative_keywords": []}
