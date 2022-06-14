FROM python:3.8.10

WORKDIR /User

COPY ./ ./

ENV PYTHONPATH=/User

RUN pip install --upgrade pip

RUN pip install "uvicorn[standard]"
RUN pip install "fastapi[all]"
RUN pip install SQLAlchemy
RUN pip install alembic
RUN pip install psycopg2-binary
RUN pip install pika