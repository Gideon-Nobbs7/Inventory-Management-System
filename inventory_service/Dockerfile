FROM python:3.12-slim AS base

WORKDIR /app

COPY ./inventory_service/requirements.txt /app/requirements.txt

# configuration for dev environment
FROM base as dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -r /app/requirements.txt 

COPY inventory_service /app

COPY ./inventory_service/entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8003" ]


# configuration for production environment
FROM base as production

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN useradd -r nduser

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r /app/requirements.txt

COPY inventory_service /app

COPY ./inventory_service/entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

RUN chmod -R 755 /app

RUN chown -R nduser:nduser /app

ENTRYPOINT [ "/app/entrypoint.sh" ]

USER nduser

EXPOSE 8003

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8003" ]


