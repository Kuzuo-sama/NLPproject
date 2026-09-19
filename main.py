from pathlib import Path
import string

import spacy
from nltk.stem import RSLPStemmer
from spacy import displacy


MODEL_NAME = "pt_core_news_sm"
EXAMPLE_TEXT = (
    "A Ana Silva visitou a empresa TechNova, em Lisboa, e investiu "
    "1.500 euros no novo projeto."
)


def load_model():
    """Carrega o modelo portugues instalado pelo comando de setup."""
    try:
        return spacy.load(MODEL_NAME)
    except OSError as error:
        raise RuntimeError(
            f"Modelo {MODEL_NAME!r} nao encontrado. "
            f"Execute: python -m spacy download {MODEL_NAME}"
        ) from error


def preprocess(text: str, nlp) -> str:
    """Devolve texto pronto para um modelo: lowercase, lemmas e filtragem."""
    doc = nlp(text.lower())
    return " ".join(
        token.lemma_.lower()
        for token in doc
        if not token.is_punct and not token.is_stop and token.lemma_.strip()
    )


def show_analysis(nlp, text: str = EXAMPLE_TEXT) -> None:
    doc = nlp(text)
    stemmer = RSLPStemmer()

    print(f"Texto: {text}\n")
    print("1. Tokenizacao:")
    print([token.text for token in doc])

    print("\n2. Stop words:")
    print([(token.text, token.is_stop) for token in doc])

    print("\n3. Stemming vs. lematizacao:")
    print("palavra | stem (RSLP) | lemma (spaCy)")
    for token in doc:
        if token.is_alpha:
            print(f"{token.text:12} | {stemmer.stem(token.text):12} | {token.lemma_}")

    print("\n4. POS tagging:")
    print([(token.text, token.pos_, token.tag_) for token in doc])
    print("Nomes proprios (PROPN):", [token.text for token in doc if token.pos_ == "PROPN"])

    print("\n5. Entidades nomeadas:")
    print([(entity.text, entity.label_) for entity in doc.ents])
    entity_html = displacy.render(doc, style="ent", jupyter=False)
    Path("entities.html").write_text(
        "<html><head><meta charset='utf-8'><title>Entidades</title></head>"
        f"<body>{entity_html}</body></html>",
        encoding="utf-8",
    )
    print("Visualizacao NER guardada em entities.html")

    print("\n6. Pre-processamento completo:")
    print(preprocess(text, nlp))


if __name__ == "__main__":
    show_analysis(load_model())