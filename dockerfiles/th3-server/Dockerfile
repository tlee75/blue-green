FROM python:3.8.19-slim-bullseye

RUN apt update -y && pip install --upgrade pip

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python3 -m pip install -r requirements.txt

COPY ./th3-server /app

CMD ["python3","/app/th3-server.py"]
