FROM python:3.8.19-slim-bullseye
ARG IMAGE_TAG_ARG
ENV IMAGE_TAG=$IMAGE_TAG_ARG

RUN apt update -y && pip install --upgrade pip

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python3 -m pip install -r requirements.txt

COPY ./th3-server /app

CMD ["python3","/app/th3-server.py"]
