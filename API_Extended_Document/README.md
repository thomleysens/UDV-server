# Description of the architecture

## MVC Architecture

The API **Extended Document** is based on a MVC architecture, which means 
we have three main parts :
- the **Model** 
- the **View**
- the **Controller**

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

Because we do not have to write sql request, we need to indicate relation between 
object directly in their python code. 

To do that we use the library call [[sqlalchemy|htps://www.sqlalchemy.org]] 
If you wat to install the library got to ###

A complete tutorial about ORM and sqlalchemy can be find [[here|https://docs.sqlalchemy.org/en/latest/orm/tutorial.html]]

We use in the application a model where all our classes have an associated table, defined like this 
('extended_document' is the name of the DB class):

```python
class ExtendedDocument(Base):
    __tablename__ = "extended_document"
```

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
