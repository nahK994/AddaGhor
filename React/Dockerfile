FROM python:3.8.10

WORKDIR /usr/src/app

# RUN cd /usr/src/app

COPY . .

RUN pip install -r requirments.txt

RUN alembic upgrade head

RUN export PYTHONPATH='/usr/src/app'

# RUN python3 app/consumer.py

# CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002" ]