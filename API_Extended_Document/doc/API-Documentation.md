# Preamble

This document presents all the functionalities provided by the API Extended Document.
This API is available on this [server](http://rict.liris.cnrs.fr:9095/).

***Note***: 
In the following, we consider that the default route is `http://rict.liris.cnrs.fr:9095`.
However if you do not want to use this server, you can run your own localhost server by following 
[these instructions](../INSTALL.md).
The routes presented in the following will remain valid.

# Available functionalities

## Extended Document functionalities

| Method | Route                                              | Description                                         |
| ------ | -------------------------------------------------- | --------------------------------------------------- |
| `POST` | [/addDocument](#adddocument)                       | Creation of a new document                          |
| `GET`  | [/getDocument/`doc_id`](#getdocument)              | Get the document with the id value is `doc_id`      |
| `GET`  | [/getDocuments](#getdocuments)                     | Get all documents matching some criteria            |
| `POST` | [/editDocument/`doc_id`](#editdocument)            | Edit the document with the the id `doc_id`          |
| `GET`  | [/deleteDocument/`doc_id`](#deletedocument)        | Delete the document with the id `doc_id`            |
| `GET`  | [/uploadFile/`doc_id`](#uploadfile)                | Redirection to update file                          |
| `POST` | [/uploadFile/`doc_id`](#uploadfile)                | Update the file associated to the document `doc_id` |
| `GET`  | [/getFile/`filename`](#getfile) | Download `filename`from the server

## Guided Tour functionalities

| Method | Route                                                       | Description                                 |
| ------ | ----------------------------------------------------------- | ------------------------------------------- | 
| `GET`  | [/addGuidedTour](#addguidedtour)                            | Creation of a guided tour                   |
| `GET`  | [/getGuidedTour/`tour_id`](#getguidedtour)                  | Get the guided tour with the id `tour_id`   |
| `GET`  | [/getGuidedTours](#getguidedtour)                           | Get the guided tours matching some criteria | 
| `GET`  | [/addDocumentToGuidedTour](#adddocumenttoguidedtour)        | Add a document to a guided tour             |
| `POST` | [/editGuidedTour/`tour_id`](#editguidedtour)                | Edit the guided tour with the id `tour_id`  |                                
| `POST` | [/editGuidedTourDocument/`tour_id`](#editguidedtourdocument)| Edit a document associated with `tour_id`   |                                
| `GET`  | [/deleteGuidedTour/`tour_id`](#deleteguidedtour)            | Delete the tour with the id `tour_id`       |

## HTTP Status Code

| Code    | Description                          |
| ------- | ------------------------------------ |
| **200** | Everything is fine                   |
| **204** | No result were found                 |
| **400** | At least one parameter is missing    |
| **404** | The resource does not exist          |
| **405** | Method not allowed                   |
| **422** | SQL integrity error (not null, etc.) |
| **500** | An internal error happen             |

# Detailed functionalities

***Note***: The type date is just a string with a certain format: `aaaa-mm-dd`

## addDocument

POST

`/addDocument`

- Create a new document with the values passed in parameters. Some of these parameters are needed.
- Return the [document](document_example.json) just created in a JSON format.

### Parameters

Any parameter can be added in the request, but only those who are effectively present
in the [document model]() will be taken into account:

| Needed | Parameter           | Type   | Description                                 |
| ------ | ------------------- | ------ | ------------------------------------------- |
| ✔️     | **title**           | string | title of the document                       |
| ✔️     | **subject**         | string | subject of the document                     |
| ✔️     | **description**     | string | description of the document                 |
| ❌     | **refDate**         | date   | date references the content of the document |
| ❌     | **publicationDate** | date   | date when the document was published        |
| ❌     | **type**            | string | type of the document (pdf, png, etc.)       |
| ❌     | **quaternionX**     | float  | X axis of the rotation of the document      |
| ❌     | **quaternionY**     | float  | Y axis of the rotation of the document      |
| ❌     | **quaternionZ**     | float  | Z axis of the rotation of the document      |
| ❌     | **quaternionW**     | float  | W axis of the rotation of the document      |
| ❌     | **positionX**       | float  | X axis of the coordinates of the document   |
| ❌     | **positionY**       | float  | Y axis of the coordinates of the document   |
| ❌     | **positionZ**       | float  | Z axis of the coordinates of the document   |

*Go back to the [list of functionalities](#extended-document-functionalities)*

## getDocument

GET

`/getDocument/{doc_id}`

- Return the [document](document_example.json) whose the id is equal to `doc_id`.

### Variable

| Name       | Type    | Description        |
| ---------- | ------- | ------------------ |
| **doc_id** | Integer | Id of the document |

*Go back to the [list](#extended-document-functionalities)*

## getDocuments

GET

`/getDocuments`

- Return a [list of documents](documents_example.json) matching the criteria, given in parameter

### Parameters

| Needed | Parameter           | Type   | Research   | Description                                 |
| ------ | ------------------- | ------ | ---------- | ------------------------------------------- |
| ❌     | **title**           | string | attributes | title of the document                       |
| ❌     | **subject**         | string | attributes | subject of the document                     |
| ❌     | **description**     | string | attributes | description of the document                 |
| ❌     | **refDate**         | date   | temporal   | date references the content of the document |
| ❌     | **publicationDate** | date   | temporal   | date when the document was published        |
| ❌     | **keyword**         | date   | keyword    | keyword on which we make the research       |

On a **date** attribute, it is possible to make a temporal research, which means, we can specify an interval on whom we make the research. To do that, we simply add one of the special characters `<`and `>` after the name of the attribute. For instance, if we want all the documents with a **refDate** between the 12/07/1998 and the 15/07/2018 we can make the request: 

`../getDocuments?refDate>=1998-07-12?refDate<=2018-07-15`

We have four new parameters:

| Needed | Parameter            | Type   |
| ------ | -------------------- | ------ |
| ❌     | **refDate<**         | date   |
| ❌     | **refDate>**         | date   |
| ❌     | **publicationDate<** | date   |
| ❌     | **publicationDate>** | date   |


*Go back to the [list](#extended-document-functionalities)*

## editDocument

POST

`/editDocument/{doc_id}`

- Update the content of the document whose the id is equal to `doc_id`.
- Return the updated [document](document_example.json).

### Variable

| Name       | Type    | Description        |
| ---------- | ------- | ------------------ |
| **doc_id** | Integer | Id of the document |

### Parameters

| Needed | Parameter           | Type   | Description                                 |
| ------ | ------------------- | ------ | ------------------------------------------- |
| ❌     | **title**           | string | title of the document                       |
| ❌     | **subject**         | string | subject of the document                     |
| ❌     | **description**     | string | description of the document                 |
| ❌     | **refDate**         | date   | date references the content of the document |
| ❌     | **publicationDate** | date   | date when the document was published        |
| ❌     | **type**            | string | type of the document (pdf, png, etc.)       |
| ❌     | **quaternionX**     | float  | X axis of the rotation of the document      |
| ❌     | **quaternionY**     | float  | Y axis of the rotation of the document      |
| ❌     | **quaternionZ**     | float  | Z axis of the rotation of the document      |
| ❌     | **quaternionW**     | float  | W axis of the rotation of the document      |
| ❌     | **positionX**       | float  | X axis of the coordinates of the document   |
| ❌     | **positionY**       | float  | Y axis of the coordinates of the document   |
| ❌     | **positionZ**       | float  | Z axis of the coordinates of the document   |

*Go back to the [list](#extended-document-functionalities)*

## deleteDocument

POST

`/deleteDocument/{id of the document}`

Delete the document whose the id is equal to `doc_id`

### Variable

| Name       | Type    | Description        |
| ---------- | ------- | ------------------ |
| **doc_id** | Integer | Id of the document |

*Go back to the [list](#extended-document-functionalities)*

## uploadFile 

GET

`/uploadFile/{doc_id}`

- Redirect on an html page from whom we can upload a file to the server
- When we push the button `upload` it will send the post request just below.
- The file is send using `form data`

POST

`/uploadFile/{doc_id}`

- Upload to the server a file, it will be save as `{doc_id}.{ext}` where `ext` is the extension of the original file.

*Go back to the [list](#extended-document-functionalities)*

### getFile

GET

`getFile/{filename}`

- Download the file, if it exists, located in the server whose name is `filename`

### Variable

| Name     | Type   | Description             |
| -------- | ------ | ----------------------- |
| filename | string | name of the file to get |

*Go back to the [list](#extended-document-functionalities)*

## addGuidedTour

GET

`/addGuidedTour`

- Create a new guided tour with the values passed in parameters.
- Return the [guided tour](guided_tour_example.json) just created in a JSON format.

### Parameters

| Needed | Parameter       | Type   | Description                    |
| ------ | --------------- | ------ | ------------------------------ |
| ✔️     | **name**        | string | Name of the guided tour        |
| ✔️     | **description** | string | Description of the guided tour |

*Go back to the [list of functionalities](#guided-tour-functionalities)*

## getGuidedTour

GET

`/getGuidedTour/{tour_id}`

- Return the [guided tour](guided_tour_example.json) whose the id is equal to `tour_id`.

### Variable

| Name        | Type    | Description        |
| ----------- | ------- | ------------------ |
| **tour_id** | Integer | Id of the document |

*Go back to the [list](#guided-tour-functionalities)*

## getGuidedTours

GET/POST

`/getGuidedTours`

- Return [all guided tours](guided_tours_example.json)

*Go back to the [list](#guided-tour-functionalities)*

## addDocumentToGuidedTour

GET

`/addDocumentToGuidedTour`

- Add the document whose id is equal to `doc_id` to the guided tour whose the id is equal to `tour_id`.
- Return the updated [guided tour](guided_tour_example.json)

### Parameters

| Needed | Parameter   | Type   | Description           |
| ------ | ----------- | ------ | --------------------- |
| ✔️     | **tour_id** | string | ID of the guided tour |
| ✔️     | **doc_id**  | string | ID of the document    |

*Go back to the [list](#guided-tour-functionalities)*

## editGuidedTour

GET

`/editGuidedTour/tour_id`

- Update the guided tour whose the id is equal to `tour_id`
- Return the updated [guided tour](guided_tour_example.json)

### Variable

| Name       | Type     | Description          |
| ---------- | -------- | -------------------- |
| **tour_id** | Integer | Id of the guided tour|

### Parameters

| Needed | Parameter       | Type   | Description                    |
| ------ | --------------- | ------ | ------------------------------ |
| ✔️     | **name**        | string | Name of the guided tour        |
| ✔️     | **description** | string | Description of the guided tour |

*Go back to the [list](#guided-tour-functionalities)*

## editGuidedTourDocument

POST

`/editGuidedTourDocument/tour_id`

### Variable

| Name       | Type     | Description          |
| ---------- | -------- | -------------------- |
| **tour_id** | Integer | Id of the guided tour|

### Parameters

| Needed | Parameter        | Type    | Description                                 |
| ------ | -----------------| ------- | ------------------------------------------- |
| ✔️     | **doc_position** | integer | Position of the document in the guided tour |
| ❌     | **text1**        | string  | information text 1 about the document       |
| ❌     | **text2**        | string  | information text 2 about the document       |
| ❌     | **title**        | string  | title of the document in the guided tour    |

*Go back to the [list](#guided-tour-functionalities)*

## deleteGuidedTour

GET

`/deleteGuidedTour/tour_id`

- Delete the guided tour whose the id is equal to `tour_id`

### Variable

| Name        | Type     | Description          |
| ----------- | -------- | -------------------- |
| **tour_id** | Integer | Id of the guided tour|

*Go back to the [list](#guided-tour-functionalities)*


# Limitations

## Route names

The names of the routes are not relevant and do not respect totally the 
[REST specifications](https://msdn.microsoft.com/en-us/library/dd203052.aspx). 
You can find a tutorial about [Flask and REST](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask) to get more information on how we can be modify the API.

| Method   | Route                                       | Description                                    |
| -------- | ------------------------------------------- | ---------------------------------------------- |
| `POST`   | [/document](#adddocument)                   | Creation of a new document                     |
| `GET`    | [/document](#getdocuments)                  | Get all documents matching some criteria       |
| `GET`    | [/document/`doc_id`](#getdocument)          | Get the document with the id value is `doc_id` |
| `PUT`    | [/document/`doc_id`](#editdocument)         | Edit the document with the the id `doc_id`     |
| `DELETE` | [/document/`doc_id`](#deletedocument)       | Delete the document with the id `doc_id`       |

### Guided tour

| Method   | Route                                                     | Description                                 |
| -------- | --------------------------------------------------------- | ------------------------------------------- |
| `POST`   | [/guidedtour](#addguidedtour)                             | Creation of a guided tour                   |
| `POST`   | [/guidedtour/`tour_id`/document](#adddocumenttoguidedtour)| Add a document to the guided tour `tour_id` | 
| `GET`    | [/guidedtour](#getguidedtour)                             | Get the guided tours matching some criteria | 
| `GET`    | [/guidedtour/`tour_id`](#getguidedtour)                   | Get the guided tour with the id `tour_id`   |
| `PUT`    | [/guidedtour/`tour_id`](#editguidedtour)                  | Edit the guided tour with the id `tour_id`  |                                
| `PUT`    | [/guidedtour/`tour_id`/document](#editguidedtourdocument) | Edit a document associated with `tour_id`   |                                
| `DELETE` | [/guidedtour/`tour_id`](#deleteguidedtour)                | Delete the tour with the id `tour_id`       |

***Note***: You can use the **PUT** method in the same way than a **POST** method (parameters are stored in `request.form` dictionary).
