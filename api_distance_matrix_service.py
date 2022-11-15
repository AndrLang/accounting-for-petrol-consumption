import requests
from api_geocoder_service import Coordinates
import config


def get_response_distance_matrix(coordinates_source: Coordinates,
                                 coordinates_target: Coordinates) -> dict:
    url = config.DISTANCE_MATRIX_URL
    DISTANCE_MATRIX_BODY = {
        "points": [
            {
                "lat": coordinates_source.latitude,
                "lon": coordinates_source.longitude
            },
            {
                "lat": coordinates_target.latitude,
                "lon": coordinates_target.longitude
            },
        ],
        "type": "shortest",
        "sources": [0],
        "targets": [1]
    }
    return requests.post(url, json=DISTANCE_MATRIX_BODY).json()


def parse_distance(response_distance_matrix_output: dict) -> int:
    return response_distance_matrix_output["routes"][0]["distance"]


def get_distance_kilometer(parse_distance_output: int) -> float:
    return round(parse_distance_output / 1000, 2)
