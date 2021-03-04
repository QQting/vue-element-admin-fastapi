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
    sudo apt install -y git npm python-is-python3 postgresql postgresql-contrib redis-server
    ```

3. Download this repo and install dependent packages
    ```bash
    cd $HOME
    git clone https://github.com/QQting/vue-element-admin-fastapi.git

    cd $HOME/vue-element-admin-fastapi/backend/app
    pip install -r requirements.txt

    cd $HOME/vue-element-admin-fastapi/frontend
    npm install
    ```

### IP Configuration
```bash
frontend
#websocket连接的ip
vue-element-admin-fastapi/frontend/src/views/monitor/server/index.vue 
#开发环境连接的后端ip
vue-element-admin-fastapi/frontend/.env.development	
#生产环境连接的后端ip
vue-element-admin-fastapi/frontend/.env.production	

backend
#alembic的数据库连接
vue-element-admin-fastapi/backend/app/alembic/env.py
#后端的数据库连接
vue-element-admin-fastapi/backend/app/app/core/config.py
#celery的数据库连接
vue-element-admin-fastapi/backend/app/app/celery_app/celery_app.py
```

### Database Configuration

```bash
# Create a PostgreSQL account
sudo -u postgres createuser root -P adlinkros
# Create a PostgreSQL database
sudo -u postgres createdb DWDB

sudo -u postgres psql
# In psql interface, type below command:
update pg_cast set castcontext='a' where castsource ='integer'::regtype and casttarget='boolean'::regtype;
# Ctrl+D to exit psql

# Please use absolute path, for example:
export PYTHONPATH="${PYTHONPATH}:$HOME/vue-element-admin-fastapi/backend/app"
cd $HOME/vue-element-admin-fastapi/backend/app
bash prestart.sh
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
python main.py
```

celery:
```bash
cd $HOME/vue-element-admin-fastapi/backend/app
sh worker-start.sh
```

## Development SOP

frontend:

If you want to use mock, turn on '/mock-test' in the file ```.env.development```.
