# Pramana List-A HF Space — CPU-only Docker image
# Based on python:3.11-slim for small footprint
FROM python:3.11-slim

# HF Spaces expects the app to listen on port 7860
ENV PORT=7860 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Prevent langdetect from writing profile files outside /tmp
    HOME=/tmp

WORKDIR /app

# System deps: build tools for Pillow/imagehash, then clean up
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        libffi-dev \
        libglib2.0-0 \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first (better layer caching)
COPY hf-space/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model into the image so no runtime download needed
RUN python -m spacy download en_core_web_sm

# Copy only the modules we need (not the full test/data dirs)
COPY shared/ ./shared/
COPY group_a_deterministic/canonicalise.py ./group_a_deterministic/canonicalise.py
COPY group_a_deterministic/pgp_meta.py     ./group_a_deterministic/pgp_meta.py
COPY group_a_deterministic/__init__.py     ./group_a_deterministic/__init__.py
COPY group_b_nlp/lang_ner.py              ./group_b_nlp/lang_ner.py
COPY group_b_nlp/stylometry.py            ./group_b_nlp/stylometry.py
COPY group_b_nlp/style_shift.py           ./group_b_nlp/style_shift.py
COPY group_b_nlp/__init__.py              ./group_b_nlp/__init__.py
COPY hf-space/app.py                      ./app.py

# HF Spaces runs as non-root user 1000
RUN useradd -m -u 1000 user
USER user

EXPOSE 7860

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
