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


# Local
- Web
```
./script/localup
```
- Bot
```
python script/bot.py
```
