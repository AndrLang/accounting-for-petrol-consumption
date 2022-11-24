import os

from dotenv import load_dotenv

load_dotenv()

USE_ROUNDED_COORDS = False
GEOCODER_API = os.getenv("GEOCODER_API")
GEOCODER_URL = (
        'https://catalog.api.2gis.com/3.0/items/geocode?q={city_for_geocoder},'
        '{street_for_geocoder},{house_for_geocoder}&'
        'fields=items.point&key=' + GEOCODER_API
)

DISTANCE_MATRIX_API = os.getenv("DISTANCE_MATRIX_API")
DISTANCE_MATRIX_URL = (
        "https://routing.api.2gis.com/get_dist_matrix?"
        "key=" + DISTANCE_MATRIX_API + "&version=2.0"
)

host = '127.0.0.1'
user = 'postgres'
password = os.getenv("POSTGRES")
db_name = 'petrol_consumption'


