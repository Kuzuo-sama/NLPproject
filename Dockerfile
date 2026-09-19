FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DISPLAY=:99 \
    NLTK_DATA=/usr/local/share/nltk_data

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        chromium \
        python3-tk \
        x11-utils \
        xvfb \
        x11vnc \
        novnc \
        fluxbox \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && python -m spacy download pt_core_news_sm \
    && python -c "import nltk; nltk.download('rslp', download_dir='/usr/local/share/nltk_data')"

COPY . .

COPY docker/start.sh /usr/local/bin/start-app
RUN chmod +x /usr/local/bin/start-app

EXPOSE 6080 5000

CMD ["/usr/local/bin/start-app"]