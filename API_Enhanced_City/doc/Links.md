# Link management

## Entities

A conceptual link should represent a relationship between a document and any linkable object. To represent this 
concept in the database, we decided to create as many `Link` entities as there are types of linkable objects.

For the moment, the only linkable object implemented is the "city object". The link are stored in the database thanks
 to `LinkCityObject` entities.
 
## Controller

Whereas each linkable object is represented by a distinct entity in the database, a generic controller is used to 
manage every type of links.

The following text is taken from the docstring of the class :

> `LinkController` works in a generic way to handle all types of links, without
> the need to add specific code for each type. Two methods are supported to
> get and create links :
> 
> - `get_links` : retrieve all links of a specified type. The type is passed as the `target_type_name` parameter. A 
> `filters` dict can be also passed as parameter to filter results by source and/or target ids.
> - `create_link` : creates a new link of the specified type. The type is passed as the `target_type_name` parameter. 
> The parameters `source_id` and `target_id` are mandatory.
> 
> `target_type_name` refers to a string representing a possibly target type
> for a link. These strings are specified in the `target_types` dictionary as
> keys, where the values correspond to the entity class type. Possible target
> type names can be retrieved with the `get_target_types` function.

## Routes

Three routes are provided by the API to access and create links :

- `GET /link` returns all target types supported.
- `GET /link/<target_type>` returns all links of a given target type. Links can be filtered depending on their source
 or their target.
 - `POST /link/<target_type>` creates and return a new link between the specified source and target.

More detailed documentation for the routes is available on the OpenAPI specification (under the `OpenAPI2` folder).