# Install Python and PostgreSQL

[Python 3.6](https://www.python.org/downloads/) or newer is recommended and PostgreSQL can be install following 
[this](https://www.postgresql.org/docs/9.3/static/tutorial-install.html).

# Clone this repository

You need to clone this repository by typing, if you have an ssh key: `git clone git@github.com:MEPP-team/UDV-server.git`

or otherwise: `git clone https://github.com/MEPP-team/UDV-server.git`

Then you need to go to the directory **API_Extended_Document**: `cd UDV-server/API_Extended_Document`

*Note: In windows `/` is replaced by `\`*

# Create a virtual environment

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

# Install packages

Required packages for the application:
- [**psycopg2**](http://initd.org/psycopg/)
- [**Sqlalchemy**](https://www.sqlalchemy.org/)
- [**Flask**](http://flask.pocoo.org/)
- [**PyYAML**](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [**Colorama**](https://pypi.org/project/colorama/)

```
pip3 install psycopg2
pip3 install sqlalchemy
pip3 install Flask
pip3 install flask_cors
pip3 install colorama
pip3 install PyYAML
```

# Create a postgres DataBase
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

Then modify the [**config.yml**](https://github.com/MEPP-team/UDV-server/blob/master/API_Extended_Document/util/config.yml) 
file located in the [`util/`](https://github.com/MEPP-team/UDV-server/blob/master/API_Extended_Document/util) sub-directory to reflect your onfiguration. 
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
[**test**](https://github.com/MEPP-team/UDV-server/blob/master/API_Extended_Document/test)

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

*Note: It is a good practice to launch the tests before running the server, because it ensures everything works find and 
is a way to have some data in the database and facilitate the tests with the front.*

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
 * Launch the uWSGI server `uwsgi --yml Deployment/API_Extended_Document.uwsgi.yml --http-socket :9090`
