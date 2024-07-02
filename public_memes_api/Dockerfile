FROM python:3.11

RUN mkdir /public_memes_api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /public_memes_api

# комментарий ниже для docker compose, если запускать docker, то раскоментировать строку ниже
#CMD ["sh", "-c", "gunicorn public_memes_api.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"]