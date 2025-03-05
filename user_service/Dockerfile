FROM python:3.12-slim

RUN useradd -r nduser

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./user_service/requirements.txt /app/requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r /app/requirements.txt

USER nduser

COPY --chown=nduser user_service /app

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "8000" ]


