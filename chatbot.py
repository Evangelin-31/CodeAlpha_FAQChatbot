"""FAQ matching engine: preprocess -> TF-IDF vectors -> cosine similarity."""
import json
import re

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
except ImportError:  # keeps the bot usable without NLTK installed
    nltk = None
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _ensure_nltk():
    """Download NLTK data once; fall back gracefully if offline."""
    if nltk is None:
        return
    for pkg in ("stopwords", "wordnet", "omw-1.4"):
        try:
            nltk.download(pkg, quiet=True)
        except Exception:
            pass


_ensure_nltk()

try:
    STOP_WORDS = set(stopwords.words("english"))
except (LookupError, NameError):
    STOP_WORDS = {"the", "a", "an", "is", "are", "of", "to", "in", "on", "for",
                  "and", "or", "do", "does", "i", "my", "me", "can", "how", "what"}
# Keep question words that carry meaning for FAQs
STOP_WORDS -= {"when", "where", "which", "who"}

_lemmatizer = WordNetLemmatizer() if nltk else None


def _lemma(word):
    try:
        return _lemmatizer.lemmatize(word)
    except (LookupError, AttributeError):
        return word


def preprocess(text: str) -> str:
    """Lowercase, remove punctuation, drop stop words, lemmatize."""
    text = re.sub(r"[^a-z0-9\s]", " ", text.lower())
    tokens = [_lemma(t) for t in text.split() if t not in STOP_WORDS]
    return " ".join(tokens)


class FAQBot:
    def __init__(self, path="faqs.json", threshold=0.25):
        with open(path, encoding="utf-8") as f:
            self.faqs = json.load(f)
        self.threshold = threshold
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform(
            [preprocess(item["question"]) for item in self.faqs]
        )

    def ask(self, user_question: str) -> dict:
        cleaned = preprocess(user_question)
        if not cleaned:
            return {"answer": "Please type a question.", "matched": None, "score": 0.0}

        scores = cosine_similarity(self.vectorizer.transform([cleaned]), self.matrix)[0]
        best = int(scores.argmax())

        if scores[best] < self.threshold:
            top = scores.argsort()[::-1][:3]
            return {
                "answer": "Sorry, I couldn't find a good answer to that. Try rephrasing, or pick one of these:",
                "matched": None,
                "score": round(float(scores[best]), 2),
                "suggestions": [self.faqs[i]["question"] for i in top],
            }
        return {
            "answer": self.faqs[best]["answer"],
            "matched": self.faqs[best]["question"],
            "score": round(float(scores[best]), 2),
        }
