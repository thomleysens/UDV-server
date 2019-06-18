# Install using docker
Modify the .env file to match this configuration:

````
# database configuration
ordbms=postgresql
user=postgres
password=password
host=postgres
port=5432
dbname=extendedDoc
````

> *Note: the .env that is commited should not be modified because it is used by travis for CI.*  
> Please make sure when you commit your files that you do not commit the `.env` file. If you see that `.env` appears in your changelog (in the `git status` command for example), you can prevent it from being commited using the command `git update-index --assume-unchanged .env`.

Then run the following commands:

````
sudo apt-get install docker
sudo apt-get install docker-compose
sudo systemctl start docker.service
sudo docker-compose build
sudo docker-compose up
````

## Troubleshooting

### Cannot start service postgres

If you get the following error when running `sudo docker-compose up` :

````
Creating extended_doc_db ...
Creating extended_doc_db ... errorERROR: for extended_doc_db  
Cannot start service postgres: driver failed programming external connectivity on endpoint extended_doc_db 
(b3e0b552dd60e5f8dbb91d4a8d40234c7de8e9f2a621a05490896dfd0fc01411): Error starting userland proxy: 
listen tcp 0.0.0.0:5432: bind: address already in useERROR: for postgres  Cannot start service postgres: 
driver failed programming external connectivity on endpoint extended_doc_db 
(b3e0b552dd60e5f8dbb91d4a8d40234c7de8e9f2a621a05490896dfd0fc01411): 
Error starting userland proxy: listen tcp 0.0.0.0:5432: bind: address already in use
ERROR: Encountered errors while bringing up the project.
````

You need to stop your local postgresql with the command `sudo service postgresql stop`.

You can also tell postgres to not start when booting with the command `sudo update-rc.d postgresql disable`

### Could not connect to server: Connection refused

While running docker compose, if the database was successfully created but you get the following error :

```
extended_doc_api | /api
extended_doc_api | Trying to connect to Database...
extended_doc_api | Config :  postgresql://postgres:password@postgres:5432/extendedDoc
extended_doc_api | Connection failed (psycopg2.OperationalError) could not connect to server: Connection refused
extended_doc_api |      Is the server running on host "postgres" (172.22.0.2) and accepting
extended_doc_api |      TCP/IP connections on port 5432?
extended_doc_api | 
extended_doc_api | (Background on this error at: http://sqlalche.me/e/e3q8)
```

It may be because the `.env` file is not correctly configured. Please make sure that your `.env` file matches the content shown above. Then, delete the database using :

```
sudo rm -r postgres-data
```

And rebuild the containers :

```
sudo docker-compose build
sudo docker-compose up
```

# Manual install  

## Install Python and PostgreSQL

[Python 3.6](https://www.python.org/downloads/) or newer is recommended and PostgreSQL can be install following
[this](https://www.postgresql.org/docs/9.3/static/tutorial-install.html).

## Clone this repository

You need to clone this repository by typing, if you have an ssh key: `git clone git@github.com:MEPP-team/UDV-server.git`

or otherwise: `git clone https://github.com/MEPP-team/UDV-server.git`

Then you need to go to the directory **API_Extended_Document**: `cd UDV-server/API_Extended_Document`

*Note: In windows `/` is replaced by `\`*

## Create a virtual environment

Then, create a virtual env in which we put the python intereter and our dependencies (only on Python3.6 or newer):
```
python3 -m venv venv
```

On **linux**, if it fails try to run the command below first: `sudo apt-get install python3-venv`

Enter in the virtual environment,
- On **Unix**: `source venv/bin/activate`
- on **Windows**: `venv\Scripts\activate.bat`

To quit the virtual environment, just type:   `deactivate`

***Warning**: Unless explicitly, in the following you need to be in the **virtual environment**.*

## Install packages

Required packages for the application:
- [**psycopg2**](http://initd.org/psycopg/)
- [**Sqlalchemy**](https://www.sqlalchemy.org/)
- [**Flask**](http://flask.pocoo.org/)
- [**PyYAML**](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [**Colorama**](https://pypi.org/project/colorama/)

Install them usin: `pip3 install -r requirements.txt` where
`requirements.txt` contains the preceding packages.

## Create a postgres DataBase
You need to create a postgres database for instance on linux with
```
(root)$ sudo su postgres
(postgres)$ createuser citydb_user
(postgres)$ createdb -O citydb_user extendedDoc
(postgres)$ exit
```

*Note: You can also use [pgAdmin](https://www.pgadmin.org), especially on Windows.
It is a software like [PhpMyAdmin](https://www.phpmyadmin.net/) but for PostgreSQL database.
By default, it is installed with PostgreSQL: `Program Files (x86)\PostgreSQL\X.X\pgAdminX\bin\pgAdminX.exe`*

Then modify the [**.env**](.env) to reflect your onfiguration.
If you have created a new database as below, no change is needed but verify anyway everything are correct

```
ordbms: postgresql
user: citydb_user
password: password
host: localhost
port: 5432
dbname: extendedDoc
```
The port number is (usually) configured in `/etc/postgresql/X.X/main/postgresql.conf` on Linux
and in `Program Files (x86)\PostgreSQL\X.X\data\postgresql.conf` on Windows

*Note: the exact location can change depending on your own configuration.*

# Execution

## Tests

To verify everything works find, you can execute the tests files, located in the folder
[**test**](test)

By default, python will not find the local packages (such as **test** or **api**),
you need to add the location of **API_Extended_Document** to the environment variable **PYTHONPATH** .
- On **Linux**: `export PYTHONPATH="."`
- On **Windows**: `set PYTHONPATH=.`

`.` corresponds to the location of **API_Extended_Document** and can be replaced
by any path to this directory.

Then you can run any test file located in the **test** directory, for instance:
```
python3 test/document_tests.py
python3 test/guided_tour_tests.py
```

*Note: if the tests don't run, verify that you have at least Python 3.6"

*Note: It is a good practice to launch the tests before running the server,
because it ensures everything works fine and is a way to have some data in the
database and facilitate the tests with the front-end.*

## Localhost execution

If you want the server to run you can then type: `python3 api/web_api.py`

## Production execution

### Context

According to the [flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/deploy/)
it is a good practice to use a [production WSGI server](https://www.fullstackpython.com/wsgi-servers.html)

### Configure and run uWSGI

Note that this part is only valid on the server `rict.lirirs.cnrs`, because of its environment.
A more detailed set up can be find on its server and its documentation.

 * Edit and adpat `Deployment/conf/API_Extended_Document.uwsgi.yml` to obtain something similar to

   ```
   uwsgi:
     virtualenv: /home/citydb_user/Demos/DocumentDemo/venv          <--- Adapt this
     master: true
     uid: citydb_user
     gid: citydb_user
     socket: /tmp/Api_Extended_Document-server.sock
     chmod-socket: 666
     module: api.web_api:app
     processes: 1
     enable-threads: true
     protocol: uwsgi
     need-app: true
     catch-exceptions: true
     log-maxsize: 10000000
     logto2: /home/citydb_user/Demos/DocumentDemo/uWSGI-server.log  <--- Adapt this
   ```

 * Fom the directory which contains the `Deployment` directory
 * Launch the uWSGI server `(venv) $ uwsgi --yml Deployment/API_Extended_Document.uwsgi.yml --http-socket :9090`

### Save the documents located in the Database

To be sure to save your files, you can save tables into csv files:
```
psql extendedDoc -c “COPY extended_document TO ‘/tmp/extended_document-Id.csv’ DELIMITER ‘,’ CSV HEADER;”
psql extendedDoc -c “COPY visualisation TO ‘/tmp/extended_document-visualisation.csv’ DELIMITER ‘,’ CSV HEADER;” (edited)
psql extendedDoc -c “COPY metadata TO ‘/tmp/extended_document-metadata.csv’ DELIMITER ‘,’ CSV HEADER;”
```
