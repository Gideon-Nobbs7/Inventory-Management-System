FROM python:3.12-slim AS base

WORKDIR /app

COPY ./user_service/requirements.txt /app/requirements.txt

FROM base as dev 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -r /app/requirements.txt

COPY user_service /app

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

FROM base as production 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN useradd -r nduser

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r /app/requirements.txt

COPY user_service /app

RUN chmod -R 755 /app

RUN chown -R nduser:nduser /app

USER nduser

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]


