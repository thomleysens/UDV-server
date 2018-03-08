# This tool is inspired from https://github.com/Jeremy-Gaillard/CityUtils/blob/master/city_utils/import_3dcitydb.py

import sys
import yaml
import argparse
from psycopg2 import connect, sql
from psycopg2.extras import NamedTupleCursor

if __name__ == '__main__':

    # arg parse
    descr = '''Process a 3DCityDB database to create a materialized view on buildings
            of the database containing their id, geometry and optionnally their
            year of construction and year of demolition.'''
    parser = argparse.ArgumentParser(description=descr)

    cfg_help = 'Path to the database configuration file'
    parser.add_argument('db_config_path', type=str, help=cfg_help)

    temporal_help = 'Extracts temporal information of the buildings'
    parser.add_argument('-t', '--temporal', dest='temporal', action='store_true', help=temporal_help)

    args = parser.parse_args()

    # Load yml db configuration file (path temporally harcoded)
    db_config = None

    with open(args.db_config_path, 'r') as db_config_file:
        try:
            db_config = yaml.load(db_config_file)
            db_config_file.close()
        except:
            print('ERROR: ', sys.exec_info()[0])
            db_config_file.close()
            sys.exit()

    # Check that db configuration is well defined
    if (("PG_HOST" not in db_config) or ("PG_NAME" not in db_config)
        or ("PG_PORT" not in db_config) or ("PG_USER" not in db_config)
        or ("PG_PASSWORD" not in db_config) or ("MATERIALIZED_VIEW_NAME" not in db_config)):
        print(("ERROR: Database is not properly defined in '{0}', please refer to README.md"
              .format(args.db_config_path)))
        sys.exit()

    # Connect to database
    db = connect(
        "postgresql://{0}:{1}@{2}:{3}/{4}"
        .format(db_config['PG_USER'], db_config['PG_PASSWORD'], db_config['PG_HOST'],
        db_config['PG_PORT'], db_config['PG_NAME']),
        cursor_factory=NamedTupleCursor, # fetch method will return named tuples instead of regular tuples
    )

    db.autocommit = True
    # Open a cursor to perform database operations
    cursor = db.cursor()

    # Drop Materialized view if it already exists
    query = ("DROP MATERIALIZED VIEW IF EXISTS {0}").format(db_config['MATERIALIZED_VIEW_NAME'])
    cursor.execute(query)

    # Fetch Data and create materialized view
    if args.temporal:
        ##### Design choices
        # - When a date in the source database is infinity (respectively
        #   -infinity) the associated semantics is to the end of time
        #   (respecitvely from the begining of time).
        # - When a date in the source database is null we consider that the
        #   associated semantics is "unknown" (or unset) and in turn interpret
        #   it a begining of time (respectively end of time) for
        #   year_of_construction (respectively year_of_demolition).
        # - Note: using infinity/-infinity instead of null to carry the
        #   semantics of "end of/begining of time" instead of null not only
        #   clarifies the situation but also makes the queries simpler and
        #   clearer.
        # - When computing the miminim and maximum dates of the source database
        #   (in order to establish practical time boundaries, think for example
        #   of setting upper and lower bounds to the temporal slider) we drop 
        #   (disregard) dates that are either null or +/-infinity.
        #   In the created materialized view we substitute to those source
        #   values (either null or +/-infinity) the corresponding computed
        #   minimum (respecitvely maximum) to a null or -infinity of a
        #   year_of_construction (respectively to a null or infinity of a
        #   year_of_demolition).
        #   The associated semantics are that before the minimum (known or
        #   finite) date means fromever and after the maximum (know or finite)
        #   means forever. Again, if we consider the temporal slider usage of
        #   such mapped dates the lower time boundary represents the situation
        #   at the origin of time whereas the upper time boundary represents
        #   final version of the city as expressed by the city data.
        # References:
        #  - https://stackoverflow.com/questions/8011914/how-to-represent-end-of-time-in-a-database
        # - https://stewashton.wordpress.com/2014/07/04/sql-and-date-ranges-dont-use-null/
        query = ( "SELECT MIN (year_of_construction) FROM building "
                  "   WHERE year_of_construction != '-infinity'")
        cursor.execute(query)
        MinConstructionDate = cursor.fetchone()[0]

        # WHERE year_demol != infinity
        # Extract the maximum of the existing demolition dates
        query = ( "SELECT MAX (year_of_demolition) FROM building "
                  "   WHERE year_of_demolition != 'infinity'")
        cursor.execute(query)
        MaxDemolitionDate = cursor.fetchone()[0]

        # Create query fetching id, geometries and temporal information of buildings

        query = ("CREATE MATERIALIZED VIEW {0} AS SELECT building.id AS gid, "
            "ST_Collect(surface_geometry.geometry) AS geom,"
            "COALESCE(building.year_of_construction, DATE '{1}')"
            "   AS year_const,"
            "COALESCE(building.year_of_demolition, DATE '{2}')"
            "   AS year_demol "
            "FROM building "
    	    "  JOIN thematic_surface ON"
            "     building.id=thematic_surface.building_id "
    	    "  JOIN surface_geometry ON "  # Trailing whitespace matters
            "surface_geometry.root_id=thematic_surface.lod2_multi_surface_id "
            "WHERE surface_geometry.geometry is not null"
            "  GROUP BY building.id" ).format(db_config['MATERIALIZED_VIEW_NAME'],
                                  MinConstructionDate,
                                  MaxDemolitionDate)
    else:
        # Create query only fetching id and geometries of buildings
        query = ("CREATE MATERIALIZED VIEW {0} AS SELECT building.id AS gid, "
            "ST_Collect(surface_geometry.geometry) AS geom FROM building "
    	    "JOIN thematic_surface ON building.id=thematic_surface.building_id "
    	    "JOIN surface_geometry ON surface_geometry.root_id=thematic_surface.lod2_multi_surface_id "
            "WHERE surface_geometry.geometry is not null GROUP BY building.id ").format(db_config['MATERIALIZED_VIEW_NAME'])

    cursor.execute(query)

    # Make the changes to the database persistent
    db.commit()

    # Close communication with the database
    cursor.close()
    db.close()
