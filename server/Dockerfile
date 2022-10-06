FROM python:3.10-bullseye
COPY /src /app
WORKDIR /app

RUN pip install redis

CMD [ "python3", "./server.py" ]