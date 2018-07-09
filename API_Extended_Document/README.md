# Description of the architecture

## MVC Architecture

The API **Extended Document** used to handle document and achieve all the CRUD operations is developed in python
It is based on an **MVC** (Model, View, Controller) architecture.
We use an **ORM** to persist our objects to the DataBase by using [sqlalchemy library](htps://www.sqlalchemy.org).
To create a service able to interpret HTTP request and send response to the client, we use [flask library](http://flask.pocoo.org/docs/1.0/) 

### The model (entities)
A document is composed of two main part :
- the **MetaData** such as its title, its description, etc.
- the **Visualisation** data that can allow to place it in space

Finally, to make the link between this to part we have another entity 
called **ExtendedDocument**

You can find below the scheme of the DB
![](Pictures/DocumentTypeObjectClassDiagram.png)


### The controller
The controller is used to interact with the entities. It can realize all
the CRUD (Create, Read, Update, Delete) operations.

### The view
The view is a sort of interface between a human and the application. 
By following the human's action the controller will make some operations 
in response.
In the application, the view is called **web_api.py** and can intercept
web requests and send response to them.

## ORM (Object Relational Mapping)

### Description
ORM is a way to crate a strong interaction between the objects and the Database :
When an object is modified, the modification can be easily persist to the DB without the need
to write any SQL request. That can reduce the complexity of the code and increase 
the abstraction between the application and the DB. Thus, we are independent of the type
of DB used (postgreSQL, Oracle, MySQL...)

### How to
**How can we share inheritance or foreign key notion between an object and a DB ?**

Because we do not have to write sql request, we need to indicate DB relationship between 
object directly in their python code. 

We use for that the [sqlalchemy library](htps://www.sqlalchemy.org) which uses [psycorpg2](http://initd.org/psycopg/docs/) to communicate with the PostgreSQL DataBase.

A complete tutorial about ORM with sqlalchemy can be find [here](https://docs.sqlalchemy.org/en/latest/orm/tutorial.html)

#### A simple example
We define a class called **ExtendedDocument**, this class has an associated table in the DB called **extended_document**
The types of the attributes of the class need to be specify (like Integer, String or Float)
This class has an id, which is the primary key of **extended_document**
```python
class ExtendedDocument(Base):
    __tablename__ = "extended_document"
    
    id = Column(Integer, primary_key=True)
    attribute1 = Column(String)
    attribute2 = Column(Float, nullable=False)
```

**Caution**
The notion of class attribute and object attribute can easily be mistakable with this defintion. 

```python
class ExtendedDocument(Base):
    attribute1 = 1
    attribute2 = Column(Float, nullable=False)
    self.attribute3 = 3
```

**attribute1** is a class attribute when both **attribute2** and **attribute3** are instance attribute. **Attribute3** is not present in the DB

To create a relationship between two classes, you can define, for the DB, a **foreign key**
For the object approach, you can define an explicit attribute in one class if it is a non reversible relationship or define an attribute in both classes otherwise.

For instance to indicate that **MetaData** owns a foreign key which is an id of **ExtendedDocument**
```python
id = Column(Integer, ForeignKey('extended_document.id'), primary_key=True)
```

In our example we have a relationship **One To One** between **metadata** and **extended_document** and its navigability is only from **extended_document** to **metadata**. We just have to precise in **ExtendedDocument**:
```python
metaData = relationship("MetaData", uselist=False, cascade="all, delete-orphan")
```
Extended_Document has an attribute metaData, the parameter *uselist* specify that we have only one instance of **MetaData**,, the attribute cascade simplify operations on metaData directly from ExtendedDocument (such as the deletion).

## Other directories

### log
This directory contains information of what happen during the execution of the application :
- **info.log** : information about the global application execution 
- **sqlalchemy.log** : operations between the DB and python

### persistence_unit
This directory contains some methods to facilitate interaction between the 
DB and the python objects and reduce lines of code when persisting objects.

### test
This directory is used to make tests, in order to be sure the application works well

### util
This directory global script and file to configure the application

#### config.yml
This file is used to specify information about the database

```
ordbms: <type of DB>
user: <use of the DB>
password: <user password>
host: <server hosting the db>
port: <port of the server>
dbname: <name of the database>
```

### log.py
Configure the logger of the application

### db_config.py
Configure the application by using the *config.yml* file. 

## Installation



