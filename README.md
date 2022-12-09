# Vault Management Demo

This is a demo project using Flask to create a simple web application.
The purpose of this project is to study about flask work flow, and how to interact with database using MVT model.

# Requirements
- Flask
- SQLite
- Python
- SQLalchemy
- Boostrap
- Hosting service: pythonanywhere

# Setup
- Create virtual environment to run the project
> python -m venv virt

- Activate virtual environment
> source virt/bin/activate

- After create the environment, install required libraries
> pip install -r requirements.txt

- Once finish installing, initialize database using below step
1. flask shell
2. Type in the below command
    ```      
      from app import db      
      db.create_all()
    ```
3. Exit the flask shell
4. Import the data using:
    > python utils/import_data.py

- Run the project
>   flask run


# About
Flask is a micro web framework suitable for creating quick and small web application.
It has the basic building block that enable user to start getting started.

Flask follow the MVT model

[![Alt text][[images/MVT.png](https://github.com/knguyennt/water_supply_flask/blob/main/images/MVT.png) "MVT model"]]

|Components| Description|
|----------|------------|
|Views| Receive request and handle internal logic. In this project app is views|
|Templates| Place tempalte files (HTML, ....) |
|Models | Handle data schema|

When first create project, we need to create the templates folder to hold out frontend files

The app.oy file is used as the main application to run


**To-do list**

[x] Create base project

[] Move all model define in app to another file

[] Clean code the project

[] Design the new data scheman

[] Update user experience
