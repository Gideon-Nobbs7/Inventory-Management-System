FROM python:3.12-slim

RUN useradd -r nduser

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./product_service/requirements.txt /app/requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r /app/requirements.txt

COPY product_service /app

RUN chmod -R 755 /app

RUN chown -R nduser:nduser /app

USER nduser

EXPOSE 8001

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8001"]


