import os
import requests

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
#
# source_latitude = 54.99770587584445
# source_longitude = 82.79502868652345
# target_latitude = 54.99928130973027
# target_longitude = 82.92137145996095
#
# DISTANCE_MATRIX_BODY = {
#     "points": [
#         {
#             "lat": source_latitude,
#             "lon": source_longitude
#         },
#         {
#             "lat": target_latitude,
#             "lon": target_longitude
#         },
#     ],
#     "sources": [0],
#     "targets": [1]
# }
# response_geocoder = requests.get(GEOCODER_URL)
# response_distance_matrix = requests.post(DISTANCE_MATRIX_URL,
#                                          json=DISTANCE_MATRIX_BODY)
# print(response_distance_matrix.text)
# print(response_geocoder.json())
