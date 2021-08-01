## Setup database

```
CREATE DATABASE "rank-search"
    WITH 
    OWNER = minhnt
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

COMMENT ON DATABASE "rank-search"
    IS 'search google rank for keywords';
```

## How to run app

Active venv

`source .venv/bin/activate`

Install packages

`pip install -r requirements.txt`

OR

`pip install --no-cache-dir -r requirements.txt`

Start app by flask run

`FLASK_APP=wsgi:app FLASK_ENV=production ./.venv/bin/flask run --host '0.0.0.0'`

Or start by gunicorn

`./.venv/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 wsgi:app`
