# English NLP project

O projeto demonstra tokenizacao, stop words, stemming, lematizacao, POS tagging,
NER e um pipeline de pre-processamento com spaCy. Inclui tambem uma pagina web
minima para analise de sentimento com TextBlob.

## Instalar e executar

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m spacy download pt_core_news_sm
python -c "import nltk; nltk.download('rslp')"
python main.py
```

O script imprime os resultados no terminal e cria `entities.html` com a
visualizacao NER produzida por `displacy.render(..., style="ent")`.

## Pagina de sentimento

```powershell
python app.py
```

Abrir `http://127.0.0.1:5000` no navegador e submeter uma frase. Para frases em
ingles, a aplicacao usa o TextBlob para calcular a polaridade. A polaridade fica
entre -1 e 1 e a interface classifica-a como negativa, neutra ou positiva. A
aplicacao tambem sinaliza palavras inglesas associadas a insultos e
discriminacao; esta e uma deteccao simples por vocabulario, nao uma moderacao
completa baseada em IA.

## Executar com Docker e noVNC

Com o Docker Desktop iniciado:

```powershell
docker compose up --build
```

No compose agregado, abrir `http://127.0.0.1:8082/npl/` para ver a aplicacao
no navegador através do noVNC.