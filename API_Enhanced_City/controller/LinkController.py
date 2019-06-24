from typing import Type, Dict

from sqlalchemy.orm.session import Session

from util.Exception import BadRequest

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
      as parameter to filter results by source and/or target ids.
    - `create_link` : creates a new link of the specified type. The type is
      passed as the `target_type_name` parameter. The parameters `source_id` and
      `target_id` are mandatory.

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
        source_id = filters.get('source_id')
        target_id = filters.get('target_id')
        query = session.query(target_type)
        if source_id is not None:
            query = query.filter(target_type.source_id == source_id)
        if target_id is not None:
            query = query.filter(target_type.target_id == target_id)
        return query.all()

    @staticmethod
    @pUnit.make_a_transaction
    def create_link(session, target_type_name, source_id, target_id):
        """
        Creates a link between the given document and city objects.

        :param Session session: SQLAlchemy session (auto filled)
        :param str target_type_name: The name of the target type.
        :param int source_id: ID of the source document.
        :param any target_id: ID of the target city object.
        :return: The newly created link.
        """
        target_type = LinkController.target_types.get(target_type_name)
        if target_type is None:
            raise BadRequest(f'{target_type_name} is not a valid link target.')
        new_link = target_type(source_id, target_id)
        session.add(new_link)
        return new_link
