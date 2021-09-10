# Introduction
The following project consist of a basic authentication API system made in flask and uses JWT authenticaion.

# Structure
```
.
|-- __init__.py
|-- auth.py
|-- main.py
`-- models.py

4 files
```

The `__init__.py` file consist of the initialisation of app and database.
The `auth.py` file consist of the authentication functions and views.
The `main.py` file consist of the user route to extract all users.
The `models.py` file consist of the databse ORM.


# Instruction to install

Install the dependencies by doing
```
pip install -r requirements.txt
```

Add secret key and database url to environment variables.

Run the app.