# vue-element-admin-fastapi

## Tech Stack
frontend: vue-element-admin  
backend: FastAPI, Celery, and PostgreSQL

## File Location
```
root:[vue-element-admin-fastapi]
|--frontend		#vue-element-admin
|--backend
|      |--app
|      |      |--alembic	#alembic
|      |      |--app
|      |      |      |--api
|      |      |      |      |--api_v1
|      |      |      |      |      |--api.py
|      |      |      |      |      |--endpoints
|      |      |      |      |      |--report	#excel export api 敏捷开发 
|      |      |      |      |      |      |--gen_excel.py
|      |      |      |      |      |      |--gen_report.py
|      |      |      |      |      |      |--report
|      |      |      |      |      |      |--__init__.py
|      |      |      |      |      |--system
|      |      |      |      |      |--websocket	#python-socketio,异步类视图区分命名空间
|      |      |      |      |      |      |--server.py
|      |      |      |      |--deps.py
|      |      |      |--celery_app	#celery
|      |      |      |      |--celery_app.py
|      |      |      |      |--worker
|      |      |      |      |      |--example.py
|      |      |      |--core
|      |      |      |      |--config.py
|      |      |      |      |--security.py
|      |      |      |--crud
|      |      |      |--db
|      |      |      |      |--base.py
|      |      |      |      |--session.py
|      |      |      |--extensions
|      |      |      |      |--exception.py	#全局异常捕获 暂时没有使用的需要,所以没用
|      |      |      |      |--logger.py	#替代原来的日志
|      |      |      |      |--routing.py	#重写路由器  支持exclude_dependencies参数=>支持全局登陆验证剔除login端口 或者你可以通过单独挂载一个新的路由器来避免全局变量
|      |      |      |      |--utils.py		#utils 主要使用了其中的list_to_tree
|      |      |      |--initial_data.py		#初始化数据
|      |      |      |--main.py
|      |      |      |--middleware			#中间件
|      |      |      |      |--access_middle.py		#中间件 登陆日志
|      |      |      |--models		#models 	Table
|      |      |      |--schemas		#schemas	Pydantic
|      |      |      |--tests
|      |      |      |--__init__.py
|      |      |--pyproject.toml		#项目所需要的包
|      |      |--scripts
|--logs				#日志路径
|      |--backend
|      |--celery
```

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

    cd $HOME/vue-element-admin-fastapi/backend/app
    sudo pip3 install -r requirements.txt

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
npm run dev
```

backend:
```bash
cd $HOME/vue-element-admin-fastapi/backend/app/app
export LD_LIBRARY_PATH=$HOME/vue-element-admin-fastapi/backend/app/app/api/api_v1/robots/RMT_core
python main.py
```

## Development SOP

frontend:

If you want to use mock, turn on '/mock-test' in the file ```.env.development```.
