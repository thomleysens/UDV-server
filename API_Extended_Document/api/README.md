# Web Application

## Flask

[flask](http://flask.pocoo.org/docs/1.0/) is a micro web framework developped in python. 
This framework allows us to interpret HTTP request (mainly GET and POST methods) and send appropriate response to the client.
To understand this framework, a tutorial can be found [here](http://flask.pocoo.org/docs/1.0/quickstart/#a-minimal-application).

### Minimal applicaton
We can create a file named **web_api.py** which contains the following code:
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return `index`
    
if __name__ == '__main__':
    app.run()
```
- First, we import the library and create an instance of Flask (called `app`).
- `app.route('/')` is used to redirect the user; when they access the route `<server-host>/`, 
    the function `index` is uses and sends 'index' as a response.
- We can then run the application with the line `app.run()`. *You can notice the addition of `if __name__ == '__main__':`, 
    it avoids conflicts when running on a production server.*


***Note**: `app.route()` is what we call in python a [decorator](../doc/Decorators.md)*

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

### Variables
Flask allows to specify a variable name in the url by following the format *<var-type:var-name>*

```python
@app.route('/deleteDocument/<int:doc_id>')
def delete_document(doc_id):
    Controller.delete_documents(doc_id)
    return 'success'
```

### Request Data

You can specify which method is expected when accessing to a specific route
```python
@app.route('/getDocument/<int:doc_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
```

To access data sent with these methods, use for
- **GET**: `request.args`
- **POST**: `request.form`
- **DELETE**: `request.form`

Data send with GET, POST and PUT methods are stored in a MultiDict: 
this a set of keys and values and it can exist several times the same key. Its structure is as follow:
```python
{"key1": "value1", "key2": "value2", "key1": "value3"}
```
