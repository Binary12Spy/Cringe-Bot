# Cringe-Bot

### What it do
Provide fun and entertainment for everyone...

- Uwuify mesages and text  
- Provide the *Vibe of the Day* from a Spotify playlist  
- Get suggestions on places to eat with the ***Wheel of Lunch***

### Install

Create and fill in .env file or supply environmnet vairables directly

```
python -m venv .\venv
.\venv\Scripts\activate.bat
pip install -r requirements.txt
```
***or***
```
git clone https://github.com/Binary12Spy/Cringe-Bot.git
cd Cringe-Bot
docker build -t cringe-bot .
docker run -d --name cringe-bot --env-file ./../.env cringe-bot
```

### Run

```
python bot.py
```