FROM python:3.8.10

WORKDIR /User

# RUN cd /usr/src/app

COPY ./ ./

RUN pip install -r requirments.txt

RUN alembic init alembic

RUN alembic revision -m "init"

RUN alembic upgrade head

RUN export PYTHONPATH='/User'

# CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]