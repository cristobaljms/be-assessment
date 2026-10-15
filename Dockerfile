FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt

COPY pyproject.toml README.md alembic.ini ./
COPY alembic ./alembic
COPY app ./app

RUN addgroup --system app && \
    adduser --system --ingroup app app && \
    chown -R app:app /app

USER app

EXPOSE 8000

CMD ["sh", "-c", "python -m alembic -c alembic.ini upgrade head && python -m fastapi run --host 0.0.0.0 --port 8000"]