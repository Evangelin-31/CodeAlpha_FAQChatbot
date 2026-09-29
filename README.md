# CodeAlpha_FAQChatbot

FAQ chatbot for college/university questions. It preprocesses the user's question, converts it to a TF-IDF vector, finds the most similar FAQ with cosine similarity, and shows that FAQ's answer.

## Run
```bash
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Structure
- `faqs.json` – FAQ dataset (edit this to change the topic)
- `chatbot.py` – preprocessing (NLTK), TF-IDF + cosine similarity (scikit-learn)
- `app.py` – Flask server with `/` and `/ask`
- `templates/`, `static/` – HTML, CSS, JavaScript chat UI

## Tuning
`FAQBot(threshold=0.25)` in `chatbot.py`: raise it for stricter matches, lower it to answer more loosely.
