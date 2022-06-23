# Installation
```
git clone git@github.com:XZIT-APP/backend-v2.git xzit_backend_dj
cd xzit_backend_dj
pipenv shell
pipenv install
cp .env.example .env
```

# Folder Stracture
```
project
│   README.md
│   .gitignore
|   .env.example
|   Pipfile
│
└───xzit -> django project
│   │   mixins
│   │   asgi.py
│   │   settings.py
|   |   urls.py
|   |   wsgi.py
└───authentication -> django app
|    │   migrations
|    │   __init__.py
|    |   admin.py
|    |   models.py
|    |   serializers.py
|    |   tests.py
|    |   urls.py
|    |   views.py
|____activity -> django app
|    |   migrations
|    |   __init__.py
|    |   admin.py
|    |   models.py
|    |   serializers.py
|    |   tests.py
|    |   urls.py
|    |   views.py
|_____filemanager -> django app 
|    |   __init__.py
|    |   admin.py
|    |   models.py
|    |   routers.py
|    |   serializers.py
|    |   tests.py
|    |   urls.py
|    |   views.py
|    |   viewsets.py
| 
|____|   media
|
|
└───templates
```

# Docs
You will find the doc url here `http://127.0.0.1:8000/swagger-ui`

