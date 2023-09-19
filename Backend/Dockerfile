FROM python:3.10.6

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python3 manage.py migrate
