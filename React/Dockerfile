FROM python:3.8.10

WORKDIR /usr/src/react

RUN cd /usr/src/react

COPY ./ ./

RUN pip install -r requirments.txt

RUN alembic upgrade head

RUN export PYTHONPATH='/usr/src/react'

# RUN python3 app/consumer.py

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002" ]