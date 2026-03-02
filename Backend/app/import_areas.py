from app.database_connection import SessionLocal
from app.models import Area
from geoalchemy2.shape import from_shape
from shapely.geometry import shape
import shapely.ops
from pyproj import Transformer
import json


filepath = "./data/limites-administratives-agglomeration-nad83.geojson"
def read_geojson(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


# Transformer: EPSG 32188 → 4326
transformer = Transformer.from_crs("EPSG:32188", "EPSG:4326", always_xy=True)


def transform_geometry(geom):
    return shapely.ops.transform(transformer.transform, geom)


def main():
    session = SessionLocal()

    # Prevent duplicates during development
    if session.query(Area).count() > 0:
        print("Areas already populated.")
        session.close()
        return

    area_data = read_geojson(filepath)

    for feature in area_data["features"]:
        properties = feature.get("properties", {})
        geometry = feature.get("geometry")

        if not geometry:
            continue

        # Convert GeoJSON → Shapely
        shapely_geom = shape(geometry)

        # Transform CRS
        shapely_geom = transform_geometry(shapely_geom)

        area = Area(
            name=properties.get("NOM"),
            area_type=properties.get("TYPE"),
            geometry=from_shape(shapely_geom, srid=4326)
        )

        session.add(area)

    session.commit()
    session.close()

    print("Areas successfully populated.")


if __name__ == "__main__":
    main()