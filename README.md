### Employee task management

#### Login credentials

##### Employee

- username = Royson,password = employee
- username = Rahul,password = employee
- username = Uday,password = employee

##### Admin

- username = Admin,password = Admin@123

#### How to run

- Create a virtualenv in python3
- Activate virtualenv
- Install requirements.txt via pip
- Run the Django server
- Use credentials to login

#### Additional packages

- Need to install redis

#### Celery commands

```sh
$ celery -A employee_task_management worker -l info
$ celery -A employee_task_management beat -l info
```
