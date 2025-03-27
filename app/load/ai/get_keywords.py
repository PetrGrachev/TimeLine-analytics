import spacy
from keybert import KeyBERT
from nltk.corpus import stopwords
import nltk

# Загрузка стоп-слов один раз
try:
    russian_stopwords = stopwords.words("russian")
except LookupError:
    nltk.download("stopwords")
    russian_stopwords = stopwords.words("russian")

# Инициализация spaCy и KeyBERT
nlp = spacy.load("ru_core_news_sm")
kw_model = KeyBERT("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

def lemmatize_text(text: str) -> str:
    """Нормализуем текст: лемматизация, удаление стоп-слов, пунктуации"""
    doc = nlp(text)
    return " ".join(
        token.lemma_ for token in doc
        if not token.is_stop and not token.is_punct and not token.is_space
    )

def get_keywords(feedback_texts, top_n=10):
    """Извлекает 2 лучшие и 2 худшие фразы"""
    try:
        if not feedback_texts:
            return {"positive_keywords": [], "negative_keywords": []}

        combined_text = " ".join(feedback_texts)
        cleaned_text = lemmatize_text(combined_text)

        keywords = kw_model.extract_keywords(
            cleaned_text,
            keyphrase_ngram_range=(1, 3),
            stop_words=russian_stopwords,
            top_n=top_n,
            use_mmr=True,
            diversity=0.7
        )

        if not keywords:
            return {"positive_keywords": [], "negative_keywords": []}

        keywords_sorted = sorted(keywords, key=lambda x: x[1], reverse=True)

        positive = [
            {"phrase": phrase, "score": round(score, 3)}
            for phrase, score in keywords_sorted[:2]
        ]
        negative = [
            {"phrase": phrase, "score": round(score, 3)}
            for phrase, score in keywords_sorted[-2:]
        ]

        return {
            "positive_keywords": positive,
            "negative_keywords": negative
        }

    except Exception as e:
        print("❌ Ошибка в get_keywords:", e)
        return {"positive_keywords": [], "negative_keywords": []}