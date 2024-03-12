## Project Setup

- Recommend python version
```
    3.10.12
```
- Recommend development env
```
    Ubuntu
```

### Create a virtual environment
- Inside the root directory of the project, open the terminal
- Install the <b>python3-venv</b> package, need to create virtual environment
```
    sudo apt install python3-venv
```
- create a virtual environemt
```
    python3 -m venv venv
```
- activate virtual environment

```
    source venv/bin/activate
```

### Install the dependencies

- Go inside the ml_service directory
```
    cd ml_service
```

- Install the dependencies
```
    pip install -r requirements.txt
```

### Make migrations

- Run the migrations
```
    python3 manage.py migrate
```

### Create a super user
- Run the following command and give a username, email, and password, and keep it saved for access the admin dashboard
```
    python3 manage.py createsuperuser
```

### Run the application

```
    python3 manage.py runserver
```

## Sample endpoint

http://127.0.0.1:8000

## Admin dashboard endpoint

http://127.0.0.1:8000/admin/
