FROM python:3.11

#WORKDIR /memes_api
RUN mkdir /public_memes_api

COPY public_memes_api/requirements.txt .

RUN pip install -r requirements.txt

COPY public_memes_api /public_memes_api
COPY public_memes_api/alembic.ini /public_memes_api/alembic.ini
#COPY public_memes_api/migrations /memes_api/public_memes_api/migrations
#WORKDIR /public_memes_api

#CMD ["sh", "-c", "gunicorn public_memes_api.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"]