# PowerPlant for Energy
Download the repo and extract it.

Localhost Deployment
Step 1: Install Required Libraries
Make sure you have mysql-connector-python and flask installed:

pip3 install mysql-connector-python flask pandas

Step 2: Set Up Your MySQL Database
Start XAMPP and ensure your MySQL service is running.

Create a database and table:
You can use phpMyAdmin (included with XAMPP) or a MySQL client to run the SQL commands in the 

powerplants_db.sql

To import the data, go to the powerplants table and import the file

powerplants.sql

Step 3: Run the WebApp
Change the database configuration in the powerplant_app.py in this function

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # your MySQL username
        password="",  # your MySQL password
        database="powerplants_db"
    )
    return conn

Run the webapp by running the file powerplant_app.py in either the Docker or the Python Flask IDE/Terminal.

Ploomber Cloud Deployment

Step 1
Compress the webapp folder in zip file format, make sure it has these 3 files

app.py -> contains the flask code
templates/index.html -> contains the web gui
requirements.txt -> contains the libraries needed for the python to run

Step 2 
Create an Application
Select Flask
Upload the webapp zipped file
Wait for the Docker to deploy it
