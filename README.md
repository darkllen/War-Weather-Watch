### Install

```shell
python -m venv .venv # create virtual env
. .venv/Scripts/activate
pip install -r requirements.txt
```

### Collect ISW articles

```shell
. .venv/Scripts/activate
python Paterny/2/getISWnews.py
```

All articles would be in `isw-articles` folder