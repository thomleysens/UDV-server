# ORM (Object Relational Mapping)

## Description
ORM is a way to crate a strong interaction between the objects to be persist and the Database : 
when an object is modified, the modification can be easily persisted to the DB without the need to write any SQL request.
Such a feature can reduce the complexity of the code since it offers to increase its abstraction level 
by making it independent from the particular technology of the chosen concrete DB (postgreSQL, Oracle, MySQL...).

## How to?
**How can we share inheritance or foreign key notion between an object and a DB ?**

Although the implementation is not required to write sql requests, it still needs to indicate the relationship 
between the DB and the object directly in their python code.
For that we use the [sqlalchemy library](htps://www.sqlalchemy.org) that in turn uses the 
[psycorpg2](http://initd.org/psycopg/docs/) (as an adapter/connector) to communicate with the PostgreSQL DataBase.

We tried to make a résumé of what we use from **SQLAlchemy**, however a lot of things are not broached and can be find
[here](https://docs.sqlalchemy.org/en/latest/orm/tutorial.html).

## A simple example

In the following we create three classes : `ExtendedDocument`, `Metadata` and `DocumentGuidedTour`.

![](../doc/img/class-diagrams/ORM_Example.png)

First of all we define the class `ExtendedDocument`. 
This class has an associated table in the DB called `extended_document`. 
The (primitive) types (e.g. Integer, String or Float) of its attributes of that class need to be specified. 
This class has an id, which is the primary key of `extended_document`.
The corresponding code snippet goes
```python
class ExtendedDocument(Base):
    __tablename__ = "extended_document"

    id = Column(Integer, primary_key=True)
    attribute1 = Column(String)
    attribute2 = Column(Float, nullable=False)
```

### Class attributes and Instance attributes

Do not confuse attribute and object attribute which can easily be mistaken:

```python
class ExtendedDocument(Base):
    attribute1 = 1
    attribute2 = Column(Float, nullable=False)
    self.attribute3 = 3
```

Above, `attribute1` is a class attribute while both `attribute2` and `attribute3` are instance attributes. 
However, `attribute3` is not present in the DB because it has no `Column`.

### Relationship and Foreign key

To create a relationship between two tables, we need to define explicitly a **foreign key** in the class definition.
For the object approach, you can define an explicit attribute in one class if it is a non reversible relationship, 
or define an attribute in both classes otherwise.

#### One to One relationship

To indicate that **MetaData** owns a foreign key which is an id of **ExtendedDocument**
```python
id = Column(Integer, ForeignKey('extended_document.id'), primary_key=True)
```

In our example we have a **One To One** relationship between `extended_document` and `metadata` and 
its navigability is only from the first one to the second. 
So we create an attribute `metaData` in `ExtendedDocument` which refers to the `metadata` table 
with the correpsonding foreignkey value:

```python
metaData = relationship("MetaData", uselist=False, cascade="all, delete-orphan")
```

**Extended_Document** has an attribute metaData, the parameter *uselist* specify that we have only one instance of **MetaData**, 
the attribute cascade simplify operations on metaData directly from ExtendedDocument (such as the deletion).

#### Many to One relationship

According to the diagram above, we a **Many to One** relationship between `extendeDocGuidedTour`and `extendedDocument`. 
Furthermore, the navigation is only from `ExtendedDocGuideTour` to `ExtendedDocument`. 
Nothing more is needed in `ExtendedDocument`, we just have to define `ExtendedDocGuideTour` as below:
```python
class DocumentGuidedTour(Base):
    __tablename__ = "document_guided_tour"

    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, ForeignKey("extended_document.id"))
    
    document = relationship("ExtendedDocument")
```
The only subtlely is, because the relation is defined in the child, you cannot add the `cascade` property on  the relationship,
it will have no effect.
If we have an `extendedDocGuidedTour` still attached to an `extendedDocument`, we cannot delete the `extendedDocument`.
However, to bypass this limitation, we can modify the `ondelete` property to the Foreign Key. 
We just have to modify the `doc_id` line into 
```python 
doc_id = Column(Integer, ForeignKey("extended_document.id", ondelete="CASCADE"))
```
