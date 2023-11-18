# Cringe-Bot

### What it do
Provide fun and entertainment for everyone...

Uwuify mesages and text
Provide the *Vibe of the Day* from a Spotify playlist
Get suggestions on places to eat with the ***Wheel of Lunch***

### Install

Create and fill in .env file or supply environmnet vairables directly

```
python -m venv .\venv
.\venv\Scripts\activate.bat
pip install -r requirements.txt
```
***or***
```
docker build -t cringe-bot .
docker run --env-file .env cringe-bot
```

### Run

```
python bot.py
```


