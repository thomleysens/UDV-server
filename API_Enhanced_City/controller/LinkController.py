from typing import Type, Dict

from sqlalchemy.orm.session import Session

from util.Exception import BadRequest, NotFound

from entities.LinkCityObject import LinkCityObject

import persistence_unit.PersistenceUnit as pUnit


class LinkController:
    """
    Controller used to manage links. For the moment, only links with city
    objects are handled.

    LinkController works in a generic way to handle all types of links, without
    the need to add specific code for each type. Two methods are supported to
    get and create links :

    - `get_links` : retrieve all links of a specified type. The type is passed
      as the `target_type_name` parameter. A `filters` dict can be also passed
      as parameter to filter results by source, target ids and other properties
      of the link (depending on the type).
    - `create_link` : creates a new link of the specified type. The type is
      passed as the `target_type_name` parameter. Properties of the new link
      are specified by the `properties` dict. Among these, `source_id` and
      `target_id` are mandatory.
    - `delete_link` : deletes an existing link. The type is passed as the
      `target_type_name` parameter. The link ID is passed through the `link_id`
       parameter.


    `target_type_name` refers to a string representing a possibly target type
    for a link. These strings are specified in the `target_types` dictionary as
    keys, where the values correspond to the entity class type. Possible target
    type names can be retrieved with the `get_target_types` function.
    """

    target_types: Dict[str, Type[LinkCityObject]] = {
        'city_object': LinkCityObject
    }

    @staticmethod
    def get_target_types():
        """
        Returns all supported target type names.
        :return: All supported target type names.
        """
        return list(LinkController.target_types.keys())

    @staticmethod
    @pUnit.make_a_query
    def get_links(session, target_type_name, filters={}):
        """
        Retrieve all links related to the target type.

        :param Session session: SQLAlchemy session (auto filled)
        :param str target_type_name: The name of the target type.
        :param dict filters: A dict to specify either the source or the target
            of the link. Two keys are accepted : `source_id` and `target_id`. If
            none is provided, no filtering is performed and all links of this type
            are retrieved.
        :return: All links retrieved.
        """
        target_type = LinkController.target_types.get(target_type_name)
        if target_type is None:
            raise BadRequest(f'{target_type_name} is not a valid link target.')
        query = session.query(target_type)
        for key, value in filters.items():
            query = query.filter(target_type.get_attr(key) == value)
        return query.all()

    @staticmethod
    @pUnit.make_a_transaction
    def create_link(session, target_type_name, properties={}):
        """
        Creates a link between the given document and an instance of the target
        type.

        :param Session session: SQLAlchemy session (auto filled)
        :param str target_type_name: The name of the target type.
        :param dict properties: The properties of the link to create. The
            dictionary must include at least two keys : `source_id` and
            `target_id`. Other keys depend on the target type.
        :return: The newly created link.
        """
        target_type = LinkController.target_types.get(target_type_name)
        if target_type is None:
            raise BadRequest(f'{target_type_name} is not a valid link target.')
        try:
            new_link = target_type(**properties)
        except TypeError as e:
            raise BadRequest(e)
        session.add(new_link)
        return new_link

    @staticmethod
    @pUnit.make_a_transaction
    def delete_link(session, target_type_name, link_id):
        """
        Deletes a link with the given target type and ID.

        :param Session session: SQLAlchemy session (auto filled)
        :param target_type_name: The name of the target type.
        :param link_id: ID of the link.
        :return: The deleted link.
        """
        target_type = LinkController.target_types.get(target_type_name)
        if target_type is None:
            raise BadRequest(f'{target_type_name} is not a valid link target.')
        link = session.query(target_type).filter(
            target_type.id == link_id).one()
        if link is None:
            raise NotFound(f'Link {target_type_name}/{link_id} does not exist.')
        session.delete(link)
        return link
