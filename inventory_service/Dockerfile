FROM python:3.12-slim

RUN useradd -r nduser

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./inventory_service/requirements.txt /app/requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r /app/requirements.txt

USER nduser

COPY --chown=nduser inventory_service /app

EXPOSE 8004

COPY --chown=nduser ./inventory_service/entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]

CMD [ "python", "manage.py", "runserver", "8003" ]


