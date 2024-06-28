FROM python:3.11

RUN mkdir /api_memes

WORKDIR /api_memes

COPY ../requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "public_memes_api.main:app", "--workers", "3", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]

