# Computer Science for All Blueprint

The Computer Science for All Blueprint is resource to help NYC public school educators bring meaningful computer science (CS) education to every student in their schools.

## Setting up a development environment

Install postgres:

```
brew install postgres
```

Create a database with a user. In the terminal type, line by line:
```
psql

CREATE DATABASE blueprint;

CREATE USER doe;

GRANT ALL PRIVILEGES ON DATABASE blueprint TO doe;

\q
```

Clone this repository:

```
git clone https://github.com/nycdoe-cs4all/blueprint-learning-site.git
```

Set up a virtual environment and install requirements

```
cd blueprint-learning-site
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

Run initial migrations

```
./manage.py migrate
```

Create a superuser account that you can use to log in locally to the admin panel

```
./manage.py createsuperuser
```


Load in data about grades/subjects
```
./manage.py loaddate fixtures2.json
```

Add the `credentials.json` file the `activities` folder (ask an admin for access to the file).

## Running locally

To run the project on you computer, just `cd` into the project directory and type:

```
source env/bin/activate
./manage.py runserver
```

The site should now be available at [http://localhost:8000](http://localhost:8000)

You can see the admin site at [http://localhost:8000/admin](http://localhost:8000/admin)


## Deploying

```
git pull origin master
sudo systemctl restart gunicorn
```

If you've edited or created any static assets (js, images, css etc) you'll also need to run the following:

```
source env/bin/activate
./manage.py collectstatic
```

