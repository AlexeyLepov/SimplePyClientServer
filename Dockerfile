FROM python:3
COPY /src /app
WORKDIR /app
CMD [ "python", "./server.py" ]