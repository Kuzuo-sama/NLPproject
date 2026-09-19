import re

from flask import Flask, render_template, request
from textblob import TextBlob


app = Flask(__name__)

INSULT_WORDS = {
    "ass", "asshole", "bastard", "bitch", "bullshit", "dumb", "idiot",
    "incompetent", "loser", "moron", "stupid", "trash",
}
DISCRIMINATION_WORDS = {
    "antisemitism", "discrimination", "homophobia", "homophobic", "racism",
    "racist", "sexism", "sexist", "xenophobia", "xenophobic",
}


def detect_content(text: str) -> str:
    """Detecta sinais simples de insulto ou linguagem discriminatoria em ingles."""
    words = {
        word.lower()
        for word in re.findall(r"[a-zA-Z]+", text)
    }
    if words & DISCRIMINATION_WORDS:
        return "discriminatorio"
    if words & {word.strip() for word in INSULT_WORDS}:
        return "insulto"
    return "normal"


def analyze_sentiment(text: str) -> float:
    """Analisa frases em ingles com o TextBlob."""
    return round(TextBlob(text).sentiment.polarity, 3)


@app.route("/", methods=["GET", "POST"])
def sentiment():
    text = ""
    polarity = None
    label = None
    content_label = None
    if request.method == "POST":
        text = request.form.get("text", "").strip()
        if text:
            content_label = detect_content(text)
            polarity = analyze_sentiment(text)
            if content_label == "insulto" and polarity >= 0:
                polarity = -1.0
            label = "positivo" if polarity > 0 else "negativo" if polarity < 0 else "neutro"
    return render_template(
        "sentiment.html",
        text=text,
        polarity=polarity,
        label=label,
        content_label=content_label,
    )


if __name__ == "__main__":
    app.run(debug=True)