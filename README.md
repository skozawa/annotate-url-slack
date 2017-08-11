# Deploy
- update & restart
```
fab -H XXX.XXX.XXX.XXX deploy
```
- update
```
fab update
```
- nginx reload
```
fab nginx:reload
```


# Setup
- install python
```
pyenv install
```

- venv & install requirements
```
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

- setup db
```
./script/setup_db
```


# Local
- Web
```
./script/localup
```
- Bot
```
python script/bot.py
```
