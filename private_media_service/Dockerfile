FROM python:3.11

RUN mkdir /private_media_service

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /private_media_service

# комментарий ниже для docker compose, если запускать docker, то раскоментировать строку ниже
#CMD ["gunicorn", "private_media_service.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8001"]