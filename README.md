# SOCIAL NETWORK - WEB APPLICATION

![](https://img.shields.io/badge/Python-14354C?style=flat&logo=python&logoColor=white)
![](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)
![](https://img.shields.io/badge/JavaScript-323330?style=flat&logo=javascript&logoColor=F7DF1E)
![](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)

## INSTALLATION

### INSTALL pip
```sh
 python3 -m pip install --upgrade pip
```

### INSTALL virtualenv
```sh
 pip install virtualenv
```

 - In ROOT project directory : 
```sh
 python -m venv venv 
```
  - THEN GO TO : 
```sh
cd venv/Scripts  THEN  .\activate
```

### CONFIGURE VSCODE DEBUG
>> Access "Python: Select Interpreter" on your VS Code settings
(ctrl+shift+p or clicking on the Python version on the status bar) and change the interpreter to the one located inside your virtualenv.

### Install Requirements Package
```sh
 pip install -r requirements.txt
```

### Migrate Database
- Delete the old  db.sqlite3 file (if you are reseting DB)
```sh
 python manage.py makemigrations network
 python manage.py migrate
```

### Create Super User
```sh
 python manage.py createsuperuser
```
>>EXAMPLE:
Username: admin
Email address: admin@admin.com
Password: admin

### FINISH
```sh
python manage.py runserver
```