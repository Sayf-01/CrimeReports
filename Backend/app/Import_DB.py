import psycopg2
from app.models import Crime, Area
from app.database_connection import SessionLocal
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from datetime import datetime

import json
filepath = "./data/Criminels.geojson"
def read_geojson_with_json(filepath):
    """
    Reads a GeoJSON file and returns a Python dictionary
    """
    try:
        # Use 'with open()' to ensure the file is closed automatically
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from the file '{filepath}'. Check file format.")
        return None

# Example usage:
geojson_data = read_geojson_with_json(filepath)

session = SessionLocal()

if geojson_data:
    # Access data like a normal Python dictionary
    print(f"GeoJSON type: {geojson_data.get('type')}")
    # Iterate through features if it is a FeatureCollection
    if geojson_data.get('type') == 'FeatureCollection' and 'features' in geojson_data:
        for i, feature in enumerate(geojson_data['features']):
            try:
                properties = feature.get('properties', {})
                geometry = feature.get('geometry', {})
                geometry_type = geometry.get('type')
                coordinates = geometry.get('coordinates', [None, None])

                if geometry_type != 'Point' or not coordinates:
                    continue  # Skip non-Point geometries

                Category = properties.get('CATEGORIE')
                date = properties.get('DATE')
                quart = properties.get('QUART')
                long, lat = coordinates


                if (not Category) or (not date) or (not quart) or (not long) or (not lat):
                        continue

                # Convert date string to datetime.date
                try:
                    date_obj = datetime.strptime(date, "%Y-%m-%d").date()
                except:
                    continue  # skip if invalid date


                point = Point(long, lat)
                geom = from_shape(point, srid=4326)
                # Find the area containing this point
                area = session.query(Area).filter(
                    Area.geometry.ST_Contains(geom)
                ).first()

                if not area:
                    continue

                crime = Crime(
                    Category=Category,
                    date=date_obj,
                    quart=quart,
                    geom=geom,
                    area_id=area.id
                )
                session.add(crime)
            except Exception as e:
                print(f"Error processing feature {i}: {e}")
                
        session.commit()
        session.close()






