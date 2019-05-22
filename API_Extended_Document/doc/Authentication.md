# Using authentication in routes

In order to know if a user has the authorization to make a request, we decided
to use the OAuth2 protocol with a JWT exchange. If a client who makes a request
to the server wants to authenticate, they must provide in a HTTP header
a JWT which proves their identity.

## Marking a route as secured

In order for a route to require authentication, you can simply add the
`@need_authentication` pattern after the `app.route`. It will check the
existence and the validity of a JWT, and if it manages to decode it, will
pass the user information as a `auth_info` parameter. Here is an example of a route
which uses this decorator :

```python
# code from `api/web_api.py`

@app.route('/user/me', methods=['GET'])
@need_authentication
def get_connected_user(auth_info):
    return send_response(
        lambda: UserController.get_user_by_id(auth_info['user_id']))()
```

## Requiring role privileges

//TODO

## Requiring owner provileges

//TODO