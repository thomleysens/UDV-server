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
        # Create query fetching id, geometries and temporal information of buildings
        query = ("CREATE MATERIALIZED VIEW {0} AS SELECT building.id AS gid, "
            "ST_Collect(surface_geometry.geometry) AS geom, building.year_of_construction "
            "AS year_const, building.year_of_demolition AS year_demol FROM building "
    	    "JOIN thematic_surface ON building.id=thematic_surface.building_id "
    	    "JOIN surface_geometry ON surface_geometry.root_id=thematic_surface.lod2_multi_surface_id "
            "WHERE surface_geometry.geometry is not null GROUP BY building.id ").format(db_config['MATERIALIZED_VIEW_NAME'])
    else:
        # Create query only fetching id and geometries of buildings
        query = ("CREATE MATERIALIZED VIEW {0} AS SELECT building.id AS gid, "
            "ST_Collect(surface_geometry.geometry) AS geom FROM building "
    	    "JOIN thematic_surface ON building.id=thematic_surface.building_id "
    	    "JOIN surface_geometry ON surface_geometry.root_id=thematic_surface.lod2_multi_surface_id "
            "WHERE surface_geometry.geometry is not null GROUP BY building.id ").format(db_config['MATERIALIZED_VIEW_NAME'])

    cursor.execute(query)
