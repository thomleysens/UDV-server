# Preamble

The aim of this page is to explain how we use decorators inside the API Extended Document and to show how powerful they are.

The objective of a decorator is to avoid writing several times the same procedure. A Decorator is used to make some operation before and after the function.

# Function without parameter

We have a function **print_call** which prints `call` and we want to print `before the call` before its execution and `after the call` after.
The first approach will be to add directly the new print lines directly inside the code of **print_call** function, however if we want to do that to several functions it can become very painful.

That's why we use a decorator. This is a function with a typical structure, like this : 
```python
def my_decorator1(old_function):
    def new_function():
        print("before the call")
        old_function()
        print("after the call")

    return new_function
```
The decorator is a function that take another function in parameter, called here `old_function`, and return a new one, called here `new_function`. 

To tell python that we want to decorate **print_call**, we had the line `@my_decorator`above the definition of the function (`my_decorator1`corresponds to the name of the decorator). So we change the definition of **print_call** to :
```python
@my_decorator1
def print_call():
    print("call")
```

Now we can call the function **print_call** like we usually do:
```python
>>> print_call()
before the call
call
after the call
```

In term of process this is equivalent to :
```python
def print_call():
    print("call")

def new_function():
    print("before the call")
    print_call()
    print("after the call")

new_function()
```

# Function with fixed parameter(s)

It is possible to have a function that needed some parameters to work. For instance we want a function that prints the name of the user and we want to display the content of some variables one before and the other after

```python
@my_decorator2
def print_user_name(user_name):
    print("Your name is", user_name)
```

The associated decorator is :

```python
def my_decorator2(old_function):
    def new_function(param1, param2, name):
        print(param1)
        old_function(name)
        print(param2)

    return new_function
```

And then we can call **print_user_name** and **print_user_age**:
```python
>>> print_user_name("before", "after", "Luke")
before
Your name is Luke
after
```

In term of process this is equivalent to :
```python
def print_user_name(name):
    print("Your name is", name)


def new_function(param1, param2, name):
    print(param1)
    print_user_name(name)
    print(param2)

new_function("before", "after", "Luke")
```

# Function with variable parameters

## Parameters `*args` and `**kwargs`

As we have seen, decorators are very useful when we have the same procedure for many functions, but so far, functions have the same parameters. If we have two functions we different number of parameter, whe cannot use classical function parameters. However, in python we have two special parameters, often calls `args` and `kwargs`, we define a function like this:
```python
def print_arguments(*args, **kwargs):
    print("args", type(args), args)
    print("kwargs", type(kwargs), kwargs)
```
When we call this function:
```python
>>> print_arguments(1, param2=2)
args <class 'tuple'> (1, )
kwargs <class 'dict'> {'param2': 2}
```
As we can see, we have two types of parameters: 
- the positional parameters, like `1` which are stored inside the tuple **args** 
- the keyword parameters like `param2: 2` which are stored inside the dictionary **kwargs**

***Note**: The number of `*` is ascending: `function(arg, *arg1, **arg2)` is correct but `function(arg, **arg2, *arg1)` is wrong.*

## Decorator with `*args` and `**kwargs`

Thanks to what it is above we can create a new decorator and a new function:
```python
def my_decorator3(old_function):
    def new_function(*args, **kwargs):
        print(args[0])
        old_function(*args, **kwargs)
        print(kwargs["key"])

    return new_function

@my_decorator3
def print_user_name(*args, **kwargs):
    print("Your name is", kwargs["name"], "and you are", args[1])
```

We can call our new function:
```python
>>> print_user_name("before", 42, name="Bond", key="after")
before
Your name is Bond and you are 42
after
```
In this example, every parameter are send to the function that is decorated `old_function(*args, **kwargs)` but it can be totally possible to send only a part of the parameters or even other parameters.

***Note**: define `old_function(args, kwargs)` in the decorator can produce unexpected result because, in this case we send two parameters: the first one is a tuple and the second one is a dictionary. However, you can remove the `*` in the definition of the decorated function too, but it means that you cannot add additional position attributes in the decorator because tuples in python are immutable.*

# Decorators in API Extended Document

We use decorators in 
[web_api.py](../api/web_api.py)
in order to handle more easily the management of exceptions. So in term of structure, we want to execute some code inside a `try...except` block in a the same way whatever the code to execute.

```python
def send_response(old_function):
    def new_function(*args, **kwargs):
        try:
            return jsonify(old_function(*args, **kwargs))
        except psycopg2.IntegrityError:
            return 'integrity error', 422
        except sqlalchemy.orm.exc.NoResultFound:
            return 'no result found', 204
        except Exception as e:
            info_logger.error(e)
            return "unexpected error", 500

    return new_function
```

The operations we want to make are procedure which are called only one time, it is not a function, for instance: 
```python
DocController.get_document_by_id(doc_id)
```

We cannot decorate this line directly, because a decorator decorate only function. That's why we use an anonymous function (also called lambda function) on whose we apply the decorator directly:

```python
send_response(lambda: DocController.get_document_by_id(doc_id))()
```

***Warning**: Do not forget `()` at the end ! Otherwise it is not a function anymore*

