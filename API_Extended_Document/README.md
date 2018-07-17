# Description of the application

# Introduction

The goal of the API **Extended Document** is to handle documents needed from the front-end in [UDV](https://github.com/MEPP-team/UDV).

It achieve all the [CRUD operations](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) on the backend side.
API Extended Document (AED) is developed in python and is based on an **MVC** (Model, View, Controller) architecture.
Persistance of objects (documents) to the DataBase is obtained through the usage of the [sqlalchemy library](https://www.sqlalchemy.org) [**ORM**](https://en.wikipedia.org/wiki/Object-relational_mapping).
In order to wrap the (CRUD) service within an HTTP protocol (to deal with the requests and send responses to the client), AED uses [flask library](http://flask.pocoo.org/docs/1.0/).

You can find below the the class diagram of the application:
![](https://raw.githubusercontent.com/wiki/MEPP-team/UDV-server/ExtendeDocumentClassDiagram.png)

In addition of this diagram, you can find the database diagram, used in relation with the class diagram:
![](https://raw.githubusercontent.com/wiki/MEPP-team/UDV-server/ExtendeDocumentDatabaseDiagram.png)

## MVC Architecture

### Model (entity)
A (UDV oriented) document is composed of two main parts :
- the **MetaData** of the document such as having a title, a description, etc.
- the **Visualisation** data that can allow e.g. to display the document   at a specified spatial position when realising a rendering of a City.

Additionally, in order to relate (link) those two parts AED uses another entity called **ExtendedDocument**.


### Controller
The controller is used to interact with the entities. It can realize all the CRUD (Create, Read, Update, Delete) operations.

### View
The view is a sort of interface between a human and the application.
By following the human's action the view informs the controller which will make some operations in response.
In the application, the view is called **web_api.py** and can intercept web requests and send response to them.

## ORM (Object Relational Mapping)

### Description
ORM is a way to crate a strong interaction between the objects to be persist and the Database : when an object is modified, the modification can be easily persisted to the DB without the need to write any SQL request.
Such a feature can reduce the complexity of the code since it offers to increase its abstraction level by making it independent from the particular technology of the chosen concrete DB (postgreSQL, Oracle, MySQL...).

### How to
**How can we share inheritance or foreign key notion between an object and a DB ?**

Although the implementation is not required to write sql requests, it still needs to indicate the relationship between the DB and the object directly in their python code.
For that we use the [sqlalchemy library](htps://www.sqlalchemy.org) that in turn uses the [psycorpg2](http://initd.org/psycopg/docs/) (as an adapter/connector) to communicate with the PostgreSQL DataBase.
A complete tutorial about ORM with sqlalchemy can be found [here](https://docs.sqlalchemy.org/en/latest/orm/tutorial.html)

#### A simple example
We define a class called **ExtendedDocument**. This class has an associated table in the DB called **extended_document**. The (primitive) types (e.g. Integer, String or Float) of the attributes of that class need to be specified. This class has an id, which is the primary key of **extended_document**.
The corresponding code snippet goes
```python
class ExtendedDocument(Base):
    __tablename__ = "extended_document"

    id = Column(Integer, primary_key=True)
    attribute1 = Column(String)
    attribute2 = Column(Float, nullable=False)
```

**Caution**
The notion of class attribute and object attribute can easily be mistaken with this definition.

```python
class ExtendedDocument(Base):
    attribute1 = 1
    attribute2 = Column(Float, nullable=False)
    self.attribute3 = 3
```

**attribute1** is a class attribute when both **attribute2** and **attribute3** are instance attribute. **Attribute3** is not present in the DB.

To create a relationship between two classes, we create a **foreign key** for the DB.
For the object approach, you can define an explicit attribute in one class if it is a non reversible relationship, or define an attribute in both classes otherwise.

For instance to indicate that **MetaData** owns a foreign key which is an id of **ExtendedDocument**
```python
id = Column(Integer, ForeignKey('extended_document.id'), primary_key=True)
```

In our example we have a relationship **One To One** between **metadata** and **extended_document** and its navigability is only from **extended_document** to **metadata**. We just have to precise in **ExtendedDocument**:
```python
metaData = relationship("MetaData", uselist=False, cascade="all, delete-orphan")
```
Extended_Document has an attribute metaData, the parameter *uselist* specify that we have only one instance of **MetaData**,, the attribute cascade simplify operations on metaData directly from ExtendedDocument (such as the deletion).

## Web Application

### Flask

[flask](http://flask.pocoo.org/docs/1.0/) is a micro web framework developped in python. This framework allows us to interpret HTTP request (mainly GET and POST methods) and send appropriate response to the client.
To understand this framework, a tutorial can be found [here](http://flask.pocoo.org/docs/1.0/quickstart/#a-minimal-application).

#### Minimal applicaton
We can create a file named **web_api.py** which contains the following code:
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'index'
```
First, we import the library and create an instance of Flask (called app).
When a user accesses the route '<server-host>/' the function sends 'index' as a response.

- During deployment, [follow the instruction](http://flask.pocoo.org/docs/1.0/deploying/#deployment) depending on your server.
- During development, to start the server, you need to execute the instructions below:
    - On **Linux**
        ```
        $ export FLASK_APP=web_api.py
        $ flask run
        ```
    - On **Windows** command prompt
        ```
        C:\path\to\app>set FLASK_APP=web_api.py
        C:\path\to\app>flask run
        ```

#### Variables

You can specify variable name in the url by following the format *<var-type:var-name>*

```python
@app.route('/deleteDocument/<int:doc_id>')
def delete_document(doc_id):
    Controller.delete_documents(doc_id)
    return 'success'
```

#### Request Data

You can specify which method is expected when accessing to a specific route
```python
@app.route('/getDocument/<int:doc_id>', methods=['GET', 'POST'])
```
Data send with GET and POST methods are stored in a MultiDict; this a set of keys and values and it can exist several times the same key. Its structure is as follow:
```python
{"key1": "value1", "key2": "value2", "key1": "value3"}
```

**GET** You can access parameters by using
```python
request.args
```

**POST** You can access parameters by using
```python
request.form
```

## Other directories

**log**
This directory contains information of what happen during the execution of the application :
- **info.log** : information about the global application execution
- **sqlalchemy.log** : operations between the DB and python

**persistence_unit**
This directory contains some methods to facilitate interaction between the
DB and the python objects and reduce lines of code when persisting objects.

**test**
This directory is used to make tests, in order to be sure the application works well

**db_config**
This directory global script and file to configure the application

**config.yml**
This file is used to specify information about the database. To use the **yml** format we use the python library named [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation)

```
ordbms: <type of DB>
user: <use of the DB>
password: <user password>
host: <server hosting the db>
port: <port of the server>
dbname: <name of the database>
```

**log.py**
Configure the logger of the application

**db_config.py**
Configure the application by using the *config.yml* file.

## Installation

Python and postgreSQL must be installed on the server

Required packages for the application:
- **sqlalchemy**
- **Flask**
- **PyYAML**

```
pip install sqlalchemy
pip install Flask
pip install PyYAML
```
