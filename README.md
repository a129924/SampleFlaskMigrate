---
title: Flask SQLAlchemy利用flask-migrate讀取DB變化
date: 2022/07/15
---

# Flask SQLAlchemy利用flask-migrate讀取DB變化

## 說明
資料庫尚未初始化或是Model結構有更新時要如何更新資料庫時，就可以使用`Flask-Migrate`。

## 建置環境
* 目前我測試環境為`python 3.9.7`
* 需先安裝pipenv套件，來管理這專案的套件，如果想知道更詳細的資料，可以查詢相關文件。
* pipenv官方文件: [pipenv官方文件](https://pipenv.pypa.io/en/latest/)
* 提供的檔案中，可以利用`requirements.txt`來安裝套件

```shell
$ pipenv install -r requirements.txt
```

## 程式碼說明
### 前言
當初看教學，是有搭配`flask-script`，但是目前此套件已沒有在更新，如果要有相同的效果，需要更改套件的程式碼，所以就找到了不用`flask-script`的用法，並讓兩個教學做整合。為了讓大家可以更快的看到效果，所以教學為sqlite。

此資料夾結構為以跟資料庫Migrate的結果如下：
```
│  app.py
│  db.sqlite3
│  manager.py
│  Pipfile
│  Pipfile.lock
│  requirements.txt
├─migrations
│  │  alembic.ini
│  │  env.py
│  │  README
│  │  script.py.mako
│  └─versions
│          190fb4900926_.py
└─project_1
    │  constants.py
    │  ext.py
    │  models.py
    │  route.py
    │  __init__.py
    └─templates
            hello.html
            
```
以下開始介紹各個程式的解說，之後再說明利用flask CLI做Migrate。

### 整併成一隻程式

---
```python=
# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
# 綁定APP跟資料庫
db = SQLAlchemy(app) 
migrate = Migrate(app,db) 
# 建立User資料庫
class User(db.Model): 
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20))

    addresses = db.relationship('Address',backref='user')
    
    def __repr__(self):
        return f"<User: {self.username}>"
# 建立Address資料庫
class Address(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email_address = db.Column(db.String(50))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f"<Email: {self.email_address}>"

# db.create_all()

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()

```

### 獨立分開程式
---
為了讓flask能夠更模組化，我嘗試讓各個不同的功能做拆分，實際運行效果與上面的`app.py`效果一模一樣。
簡易資料夾檔案結構
```
│  manager.py # 主程式
└─project_1
    │  __init__.py
    │  constants.py # 紀錄DATABASE基本資料
    │  ext.py # 宣告db
    │  models.py # 資料庫模組
    │  route.py # flask視窗圖
    └─templates
            hello.html
```
---
#### 程式碼介紹

* 宣告flask app並初始化
```python=
# __init__.py
from flask import Flask
from flask_migrate import Migrate

from project_1.route import hello
from project_1.constants import DB_URL
from project_1.ext import db

import project_1.models 



def create_app():
    app = Flask(__name__)
    migrate = Migrate()
    # 綁定APP跟資料庫，並初始化
    db.init_app(app)
    migrate.init_app(app, db)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL # 資料庫URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # 與@app.route()效果一樣
    app.add_url_rule('/',"index",hello)
    
    return app
```

* DATABASE基本資料，此範例為`sqlite`
```python=
# constants.py
# DB連線資訊

DB_URL = 'sqlite:///db.sqlite3'
```

* 宣告db
```python=
# ext.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

* 資料庫模組
```python=
# models.py
from project_1.ext import db

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20))

    addresses = db.relationship('Address',backref='user')
    
    def __repr__(self):
        return f"<User: {self.username}>"

class Address(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email_address = db.Column(db.String(50))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f"<Email: {self.email_address}>"
```

* flask視窗圖，簡單展示網站功能是否正常
```python=
# route.py
from flask import render_template

def hello():
    return render_template('hello.html',name = "ERIC")
```

### flask CLI
---
之後打開`terminal`，運行以下代碼，範例如下：
* db初始化

```shell
$ flask db init
```
建立`migrations`資料夾及相關檔案

* db遷移
```shell=
$ flask db migrate
```
建立`migrations`資料夾的`versions`底下建立一個`XXX.py`，記錄著版本的變更，並且產生`*.sqlite3`。

* db update
```shell=
$ flask db upgrade
```
將更新版本記錄上去。

* db update
```shell=
$ flask db current
```
看是否有綁定成功。

## GitHub以及參考文件
* GitHub: [範例檔案](https://github.com/a129924/SampleFlaskMigrate)
* pipenv官方文件: [官方文件](https://pipenv.pypa.io/en/latest/)
* flask-sqlalchemy官方文件: [官方文件](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#installation)
* flask-migrate官方文件: [官方文件](https://flask-migrate.readthedocs.io/en/latest/)


---
###### tags: `flask` `flask-sqlalchemy` `flask-migrate` `sqlite`

