FROM python:3.10
LABEL maintainer="asr77734@gmail.com"
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
COPY ./src /code/src
COPY ./alembic.ini /code/alembic.ini
COPY ./migrations /code/migrations
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN alembic upgrade head
CMD [ "gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:7000", "src.main:app" ]
