FROM python:3.8.10

WORKDIR /react

# RUN cd /usr/src/app

COPY ./ ./

RUN pip install virtualenv

RUN virtualenv env

RUN . env/bin/activate

RUN pip install -r requirments.txt

RUN alembic upgrade head

# RUN export PYTHONPATH='/react'

# ENV PYTHONPATH="${PYTHONPATH}:/react"
# RUN python3 app/consumer.py

# CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002" ]