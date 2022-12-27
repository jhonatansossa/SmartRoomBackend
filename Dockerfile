FROM python:3.9.15-buster

RUN apt-get update && apt-get install -y

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT ["flask"]

CMD ["run", "-h", "0.0.0.0"]



