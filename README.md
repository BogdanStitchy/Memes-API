![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-D82C20?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-003545?style=for-the-badge&logo=sqlalchemy)
![Alembic](https://img.shields.io/badge/Alembic-336791?style=for-the-badge)
![Pydantic](https://img.shields.io/badge/Pydantic-2D3748?style=for-the-badge&logo=pydantic)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Jinja2](https://img.shields.io/badge/Jinja2-B41717?style=for-the-badge&logo=jinja&logoColor=white)
![Boto3](https://img.shields.io/badge/Boto3-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)

![MinIO](https://img.shields.io/badge/MinIO-F68D2E?style=for-the-badge&logo=minio&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery)
![Flower](https://img.shields.io/badge/Flower-306998?style=for-the-badge&logo=flower)
![Prometheus](https://img.shields.io/badge/Prometheus-000000?style=for-the-badge&logo=prometheus)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![Sentry](https://img.shields.io/badge/Sentry-362D59?style=for-the-badge&logo=sentry&logoColor=white)


<p align="center">
  <img src="https://github.com/BogdanStitchy/Memes-API/assets/83240866/7094bc5a-35ad-4b7f-9a93-0898e8bca2e1" alt="мем">
</p>

# Оглавление

- [Описание проекта](#описание-проекта)
- [Технологии](#технологии)
- [Установка и запуск](#Установка-и-запуск)
- [Конфигурация](#конфигурация)
- [API Endpoints](#API-Endpoints)
- [Документация API](#Документация-API)
- [Тестирование](#Тестирование)

# Описание проекта

API для управления мемами, которое позволяет получать, добавлять, обновлять и удалять мемы, а также получать
метаданные мемов. API предоставляет возможности для постраничного получения списка мемов, а также получения нескольких
изображений мемов в одном запросе.

Проект состоит из 9 сервисов:

1) Публичный API с бизнес-логикой;
2) Приватный API для работы с медиа-файлами, используя S3-совместимое хранилище;
3) Postgresql для хранения медиа данных о мемах;
4) Minio для хранения файлов мемов;
5) Redis для кеширования и в качестве брокера для celery задач;
6) Celery для выполнения фоновых задач;
7) Flower для мониторинга статуса фоновых Celery задач;
8) Prometheus для сбора метрик работы приложения;
9) Grafana для визуализации метрик Prometheus.

# Технологии

- **FastAPI** - используется для создания REST API. FastAPI поддерживает асинхронную обработку запросов и
  автоматическую генерацию документации.

- **SQLAlchemy** - ORM, позволяющая взаимодействовать с базой данных с использованием объектно-ориентированного
  подхода. Упрощает выполнение операций с базой данных. Используется асинхронная версия (asyncpg)

- **PostgreSQL** - объектно-реляционная система управления базами данных, используемая для хранения данных о
  пользователях, отелях и бронированиях.

- **Pydantic** - используется для валидации и управления данными с использованием аннотаций типов Python.
  Обеспечивает строгую типизацию и валидацию входящих данных для API.

- **Celery** - асинхронная очередь задач, используемая для выполнения фоновых задач, таких как, например,
  удаление картинки мема из s3 хранилища.

- **Flower** - веб-интерфейс для мониторинга и управления задачами Celery. Используется для отслеживания состояния
  задач и работы воркеров.

- **Redis** - система управления базами данных в памяти, используемая в качестве брокера сообщений для Celery и для
  кэширования данных, чтобы ускорить загрузку часто запрашиваемой информации.

- **Docker** - используется для запуска приложений в контейнерах. Упрощает развертывание и управление приложением,
  обеспечивая его изоляцию от окружения.

- **Docker Compose** - используется для запуска всех сервисов проекта удобным способом.

- **Alembic** - инструмент для миграции баз данных, позволяющий версионировать и применять изменения в схеме базы
  данных.

- **Pytest** - фреймворк для написания и выполнения тестов. Используется для unit и integration тестирования.

- **Admin Panel** - интерфейс администратора, обеспечивающий удобное управление данными sql хранилища.

- **Prometheus** - система мониторинга и оповещения, используется для наблюдения за работой приложения в
  реальном времени (сбор метрик).

- **Grafana** - инструмент для визуализации и анализа данных, используется для мониторинга
  производительности приложений и систем, по средствам создания информативного дашборда (использует метрики, снятые
  Prometheus).

- **Sentry** - система отслеживания ошибок, используется для отслеживания и оповещении о проблемах в реальном времени.

# Установка и запуск

1. Клонируйте репозиторий:

```plaintext
   https://github.com/BogdanStitchy/Memes-API.git
```

2. Перейдите в директорию проекта:

```plaintext
   cd Memes-API
```

3. Для возможности запуска и проверки всех сервисов без самостоятельного создания .env файлов, .env файлы, необходимые
   для сборки и работы
   docker-compose, добавлены в корень проекта. Необходимо выполнить команды:

```bash
  docker compose build
  ```

  ```bash
  docker compose up
  ```

После запуска, публичный сервис будет доступен по адресу: **http://127.0.0.1:9001/docs**

Приватный сервис будет доступен по адресу: **http://127.0.0.1:9002/docs**

Админ панель для публичного сервиса: **http://127.0.0.1:9001/admin**

Prometheus будет доступно по адресу **http://127.0.0.1:9090/**

Grafana будет доступно по адресу **http://127.0.0.1:3000/**

Flower будет доступно по адресу **http://127.0.0.1:5555/**

# Конфигурация

## Приватный сервис

Расположение конфигурационного файла приватного сервиса: *private_media_service/config/.env*.
Содержимое файла *private_media_service/config/.env* следующее:

  ```dotenv
MODE=
LOG_LEVEL=
LOGIN_S3=
PASSWORD_S3=
HOST_S3=

  ```

Файл заполняется без кавычек. В конце обязательно должна быть пустая строка.

* MODE - режим работы приложения. Доступны следующие варианты: "DEV", "TEST", "PROD"
* LOG_LEVEL - уровень логирования приложения по умолчанию
* LOGIN_S3 - логин для s3 хранилища
* PASSWORD_S3 - пароль для s3 хранилища
* HOST_S3 - хост на котором расположено s3 хранилище

## Публичный сервис

Расположение конфигурационного файла публичного сервиса: *public_memes_api/config/.env*.
Содержимое файла *public_memes_api/config/.env* следующее:

  ```dotenv
MODE=
LOG_LEVEL=
LOGIN_DB=
PASSWORD_DB=
NAME_DB=
HOST=
DB_PORT=
DIALECT_DB=
DRIVER_DB=

TEST_LOGIN_DB=
TEST_PASSWORD_DB=
TEST_NAME_DB=
TEST_HOST=
TEST_PORT=

HOST_REDIS=
SENTRY_DNS=

PRIVATE_MEDIA_SERVICE_URL=
  
  ```

Файл заполняется без кавычек. В конце обязательно должна быть пустая строка.

* MODE - режим работы приложения. Доступны следующие варианты: "DEV", "TEST", "PROD"
* LOG_LEVEL - уровень логирования приложения по умолчанию
* LOGIN_DB - логин для базы данных
* PASSWORD_DB - пароль для базы данных
* NAME_DB - имя используемой базы данных
* HOST - хост на котором расположена используемая база данных
* DB_PORT - порт для подключения на хосте для базы данных
* DIALECT_DB - используемая СУБД. Для выбора возможных вариантов
  ознакомьтесь с [документацией](https://docs.sqlalchemy.org/en/20/core/engines.html)
* DRIVER_DB - драйвер для СУБД. Для выбора возможных вариантов
  ознакомьтесь с [документацией](https://docs.sqlalchemy.org/en/20/core/engines.html)


* TEST_LOGIN_DB - логин тестовой базы данных
* TEST_PASSWORD_DB - пароль тестовой базы данных
* TEST_NAME_DB - имя тестовой базы данных
* TEST_HOST - хост на котором расположена тестовая базы данных
* TEST_PORT - порт для подключения на хосте для тестовой базы данных


* HOST_REDIS - хост расположения redis
* SENTRY_DNS - секретный ключ для сервиса Sentry

* PRIVATE_MEDIA_SERVICE_URL - адрес приватного сервиса

## Конфигурация docker compose

### minio сервис

Расположение конфигурационного файла minio сервиса: *.env-minio*. Данный файл отвечает за конфигурацию minio сервиса в
docker compose.
Содержимое файла следующее:

 ```dotenv
MINIO_ROOT_USER=
MINIO_ROOT_PASSWORD=
  ```
* MINIO_ROOT_USER - логин minio сервиса
* MINIO_ROOT_PASSWORD - пароль minio сервиса

### Приватный сервис
  ```dotenv
MODE=
LOG_LEVEL=
LOGIN_S3=
PASSWORD_S3=
HOST_S3=
  
  ```

Переменные все те же, что и в файле *private_media_service/config/.env*.

### Публичный сервис
Переменные все те же, что и в файле *public_memes_api/config/.env*, за исключением следующих переменных:

* POSTGRES_DB - название базы данных, созданной в docker compose
* POSTGRES_USER - логин базы данных, созданной в docker compose
* POSTGRES_PASSWORD - пароль базы данных, созданной в docker compose

# API Endpoints

### Публичный сервис

- `GET /memes/` - Получение списка мемов с постраничной разбивкой.
- `GET /memes/batch_images` - Получение нескольких изображений мемов (multipart/mixed) в одном запросе.
- `GET /memes/{meme_id}` - Получение изображения мема по его ID.
- `GET /memes/{meme_id}/metadata` - Получение метаданных мема по его ID.
- `POST /memes/` - Добавление нового мема.
- `PUT /memes/{meme_id}` - Обновление метаданных и/или изображения мема.
- `DELETE /memes/{meme_id}` - Удаление мема по его ID.

- `GET /metrics` - Получение метрик (дефолтный эндпоинт Prometheus).

### Приватный сервис

- `POST /memes/upload` - Загрузка файла на сервер.
- `GET /memes/download/{filename}` - Скачивание файла с сервера.
- `GET /memes/files` - Получение списка файлов на сервере.
- `DELETE /memes/delete/{filename}` - Удаление файла с сервера.


# Документация API

После запуска приложения документация приватного API будет доступна по адресу **http://127.0.0.1/:9002/docs.**

После запуска приложения документация публичного API будет доступна по адресу **http://127.0.0.1/:9001/docs.**

# Тестирование

Установите все необходимые зависимости (находясь в корневой директории проекта):

```bash
pip install -r public_memes_api\requirements.txt
```

Для запуска тестов в Bash выполните команды (находясь в корневой директории проекта):

* для запуска тестов приватного сервиса:

```bash
pytest private_media_service\tests -v
```

* для запуска тестов публичного сервиса:
```bash
pytest public_memes_api\tests -v
```
