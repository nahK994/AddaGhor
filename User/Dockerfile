FROM python:3.6.9

WORKDIR /User

# RUN cd /usr/src/app

COPY ./ ./

RUN pip install --upgrade pip

RUN pip install -r requirments.txt

RUN alembic upgrade head

RUN export PYTHONPATH='/User'

# CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]