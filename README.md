# Flask-Bigger *Flask大型应用骨架*

## 后端说明
> 使用 **Python 3** (理论上 **Python 2**可以正常运行，但是未测试)

### 后端-使用的第三方库
* **Flask**
    - [GitHub](https://github.com/pallets/flask)
    - [PyPi](https://pypi.python.org/pypi/Flask)
    - [Doc](http://flask.pocoo.org/docs/)
    - [Doc-v0.10](http://docs.jinkan.org/docs/flask/)(中文)
    - [Doc-v0.11](http://python.usyiyi.cn/translate/flask_011_ch/index.html)(中文)
    - [Doc-v1.0.2](https://dormousehole.readthedocs.io/en/latest/)(中文)
* **Jinja2**
    - [GitHub](http://github.com/mitsuhiko/jinja2)
    - [PyPi](https://pypi.python.org/pypi/Jinja2)
    - [Doc](http://jinja.pocoo.org/docs/)
    - [Doc](http://python.usyiyi.cn/translate/jinja2_29/index.html)(中文)
    - [Doc](http://docs.jinkan.org/docs/jinja2/)(中文)

### 安装依赖包
```shell
pip install -r requirements.txt
```

### 数据库迁移
1. 初始化迁移配置
    ```shell
    python manage.py db init
    ```
2. 生成迁移文件
    ```shell
    python manage.py db migrate
    ```
3. 执行迁移操作(更改到数据库)
    ```shell
    python manage.py db upgrade
    ```
4. 查看帮助
    ```shell
    python manage.py db --help
    ```

### 安装依赖包
```shell
pip install -r requirements.txt
```

### 开发运行
```shell
python ./run.py
# 或者
python manage.py runserver --host 0.0.0.0 --port 5555

# 查看运行帮助
python manage.py runserver --help
```

---

## 前端说明

### 前端-使用的第三方库
* **Bootstrap**
    - [GitHub](https://github.com/twbs/bootstrap)
    - [Doc-com](http://getbootstrap.com)
    - [Doc](https://v3.bootcss.com)(中文)

## (关键)目录、文件说明
```
├── backend                            # 后端文件目录
│   ├── __init__.py                    # 包标识
│   ├── admin                          # 默认Admin后端(子应用)
│   │   ├── __init__.py                # 包标识
│   │   ├── main.py                    # Admin主文件
│   │   ├── models.py                  # 模型(User)
│   │   ├── secure.py                  # 安全模块(登录限制)
│   │   └── views                      # Admin视图文件夹
│   │       ├── __init__.py            # 包标识
│   │       ├── ...                    # 其他视图
│   │       └── view_user.py           # 用户视图
│   ├── app_env.py                     # 应用环境变量配置获取
│   ├── app_map.py                     # 子应用汇总入口
│   ├── apps                           # 子应用目录(结构可参考admin)
│   │   ├── ...                        # 子应用
│   │   └── __init__.py                # 包标识
│   ├── core                           # 站点核心(独立于具体业务)文件目录
│   │   ├── __init__.py                # 包标识
│   │   ├── cdn.py                     # CDN
│   │   ├── database.py                # 数据库
│   │   ├── exception.py               # 异常
│   │   ├── hook.py                    # 钩子
│   │   ├── middlewares.py             # 中间件
│   │   ├── route.py                   # 路由
│   │   └── template.py                # 模板
│   ├── startup.py                     # 站点启动入口文件
│   └── utils                          # 工具库目录
│       ├── __init__.py                # 包标识
│       ├── classes.py                 # 辅助类
│       ├── database.py                # 数据库操作辅助函数封装
│       └── functions.py               # 辅助函数
├── config                             # 外部配置
│   ├── cdn.json                       # CDN资源列表
│   ├── database.json                  # 数据库配置
│   ├── example-database-mysql.json    # 数据库配置文件示例(MySQL)
│   ├── example-database-sqlite.json   # 数据库配置文件示例(SQLite)
│   └── robots.txt                     # 搜索引擎配置文件
├── frontend                           # 文件目录
│   ├── static                         # 静态文件目录
│   │   ├── ...                        # 自定义静态文件(css,js,image)
│   │   ├── admin                      # 默认Admin前端
│   │   └── _libs                      # 第三方库
│   ├── templates                      # 模板目录
│   │   ├── ...                        # 各子应用模板
│   │   └── base-layout.html           # 基础父模板
│   ├── favicon.ico                    # 站点图标(ICO)
│   ├── favicon.png                    # 站点图标(PNG)
│   ├── flask-bigger.png               # LOGO(PNG)
│   └── robots.txt                     # 搜索引擎配置文件
├── .gitignore                         # Git忽略文件
├── deploy.py                          # 部署-启动文件
├── LICENSE                            # 许可证(MIT)
├── manage.py                          # 命令行操作脚本(数据库操作)
├── README.md                          # 项目说明
├── requirements.txt                   # 依赖包清单文件
├── run.py                             # 开发运行-启动文件
└── site.version                       # 站点版本文件
```