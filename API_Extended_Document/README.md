# Description of the application

# Introduction

The goal of the API **Extended Document** is to handle documents needed from the front-end in [UDV](https://github.com/MEPP-team/UDV).

It achieves all the [CRUD operations](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) on the backend side.
API Extended Document (AED) is developed in python and is based on an **MVC** (Model, View, Controller) architecture.
Persistance of objects (documents) to the DataBase is obtained through the usage of the [sqlalchemy library](https://www.sqlalchemy.org) [**ORM**](https://en.wikipedia.org/wiki/Object-relational_mapping).
In order to wrap the (CRUD) service within an HTTP protocol (to deal with the requests and send responses to the client), AED uses the [flask library](http://flask.pocoo.org/docs/1.0/).


**ExtendedDocument** is an object, that correspond to a (raw) document (e.g. a picture, a map, a graphic) associated with some metadata and other visualization data.
It is in the heart of the application, we can create, read, update and delete them.
On top of that, in order to respond to the 
[need 07](https://github.com/MEPP-team/RICT/blob/87610d01d87f5c6dfc2873c28de59b06b33aa31f/Doc/Devel/Needs/Need007.md)
and the [need 25](https://github.com/MEPP-team/RICT/blob/87610d01d87f5c6dfc2873c28de59b06b33aa31f/Doc/Devel/Needs/Need025.md), 
we have also the possibility to attach an **ExtendedDocument** to one or several **Guided Tours**.

You can find below the the class diagram of the application: 
![](https://raw.githubusercontent.com/wiki/MEPP-team/UDV-server/DocumentWithTourClassDiagram.png)

In addition, you can find the database diagram, used in relation with the class diagram:  
![](https://raw.githubusercontent.com/wiki/MEPP-team/UDV-server/ExtendedDocumentDatabaseDiagram.png)
*Note: This diagram was automaticaaly create using [DataGrip](https://www.jetbrains.com/datagrip/) developed by JetBrains.*

The sources can be find on the [wiki](https://github.com/MEPP-team/UDV-server/wiki)

## MVC Architecture

### Model (entity)
A (UDV oriented) document is composed of two main parts :
- the **MetaData** of the document such as having a title, a description, etc.
- the **Visualisation** data that can allow e.g. to display the document   at a specified spatial position when realising a rendering of a City.

Furthermore, we have a Many to Many relationship between **ExtendedDocument** and **GuidedTour**, that is why we have created the class **ExtendeDocGuideTour**. It can link a document to a guided tour. A document can be associated several times to the same guided tour. A guided tour has a beginning and an end, so the notion or order is very important, hence we have the attribute **doc_position**, that defines the order of each document in the guided tour.

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

### How to?
**How can we share inheritance or foreign key notion between an object and a DB ?**

Although the implementation is not required to write sql requests, it still needs to indicate the relationship between the DB and the object directly in their python code.
For that we use the [sqlalchemy library](htps://www.sqlalchemy.org) that in turn uses the [psycorpg2](http://initd.org/psycopg/docs/) (as an adapter/connector) to communicate with the PostgreSQL DataBase.

We tried to make a [résumé](https://github.com/MEPP-team/UDV-server/blob/master/API_Extended_Document/entities/README.md) of what we use from SQLAlchemy, however a lot of things are not broached and can be find 
[here](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html).

## Web Application

### Flask

[flask](http://flask.pocoo.org/docs/1.0/) is a micro web framework developped in python. This framework allows us to interpret HTTP request (mainly GET and POST methods) and send appropriate response to the client.
Some complementary information are available in 
[api folder](https://github.com/MEPP-team/UDV-server/tree/master/API_Extended_Document/api)
Moreover, you can find a tutorial [here](http://flask.pocoo.org/docs/1.0/quickstart/#a-minimal-application).

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

