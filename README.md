# vue-element-admin-fastapi

## Prerequisite

1. Ubuntu 20.04

2. Tools and Packages for Development
    ```bash
    sudo apt update
    sudo apt install -y git npm python-is-python3
    ```

3. Download this repo and install dependent packages
    ```bash
    cd $HOME
    git clone https://github.com/QQting/vue-element-admin-fastapi.git

    cd $HOME/vue-element-admin-fastapi/backend/lib
    sudo dpkg -i *.deb

    cd $HOME/vue-element-admin-fastapi/backend/app
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
    poetry install

    cd $HOME/vue-element-admin-fastapi/frontend
    npm install
    ```

### IP Configuration

You can skip below steps if you don't need to modify the server IP and Port.

```bash
frontend
# for websocket connection
vue-element-admin-fastapi/frontend/src/views/monitor/server/index.vue 
# for development env
vue-element-admin-fastapi/frontend/.env.development	
# for production env
vue-element-admin-fastapi/frontend/.env.production	

backend
# for web-admin & database
vue-element-admin-fastapi/backend/app/app/core/config.py
# for celery
vue-element-admin-fastapi/backend/app/app/celery_app/celery_app.py
```

## Start SOP

frontend:
```bash
cd $HOME/vue-element-admin-fastapi/frontend
./start_frontend.sh
```

backend:
```bash
cd $HOME/vue-element-admin-fastapi/backend
./start_backend.sh
```

## Development SOP

frontend:

If you want to use mock, turn on '/mock-test' in the file ```.env.development```.

Unit test for backend:

```bash
cd $HOME/vue-element-admin-fastapi/backend/app/app/tests/api/api_v1
pytest-3 test_robot.py -s -v
```
