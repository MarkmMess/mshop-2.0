FROM python:3.13.5-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app:/app/src

RUN pip install --upgrade pip wheel "poetry==2.2.1"
RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root --no-interaction

COPY src ./src

RUN chmod +x src/prestart.sh

CMD ["src/prestart.sh"]