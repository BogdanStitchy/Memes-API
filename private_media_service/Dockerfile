FROM python:3.11

RUN mkdir /s3_memes

WORKDIR /s3_memes

COPY ../requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "private_media_service.main:app", "--workers", "3", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8001"]

