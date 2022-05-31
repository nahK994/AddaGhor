FROM python:3.8.10

WORKDIR /User

# RUN cd /usr/src/app

COPY ./ ./

ENV PYTHONPATH=/User

RUN pip install --upgrade pip

# RUN pip install -r requirments.txt
RUN pip install "uvicorn[standard]"
RUN pip install "fastapi[all]"
RUN pip install SQLAlchemy
RUN pip install alembic
RUN pip install psycopg2-binary
RUN pip install pika

RUN alembic upgrade head

# CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]