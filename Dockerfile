FROM python:3.10.13-alpine3.18

WORKDIR /app

ADD bot.py .
ADD requirements.txt .
ADD cogs/ ./cogs

RUN pip install -r requirements.txt

CMD [ "python", "./bot.py" ]