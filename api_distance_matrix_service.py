import sys
import requests
from api_geocoder_service import Coordinates
import config


def get_distance_kilometer(parse_distance_output: int) -> float:
    return round(parse_distance_output / 1000, 2)


def parse_distance(response_distance_matrix_output: dict) -> int:
    return response_distance_matrix_output["routes"][0]["distance"]


def get_response_distance_matrix(coordinates_departure: Coordinates,
                                 coordinates_arrival: Coordinates) -> dict:
    url = config.DISTANCE_MATRIX_URL
    DISTANCE_MATRIX_BODY = {
        "points": [
            {
                "lat": coordinates_departure.latitude,
                "lon": coordinates_departure.longitude
            },
            {
                "lat": coordinates_arrival.latitude,
                "lon": coordinates_arrival.longitude
            },
        ],
        "type": "shortest",
        "sources": [0],
        "targets": [1]
    }
    return requests.post(url, json=DISTANCE_MATRIX_BODY).json()


if __name__ == "__main__":
    try:
        print(get_distance_kilometer(parse_distance(get_response_distance_matrix(
            Coordinates(latitude=55.75142, longitude=37.615606),
            Coordinates(latitude=55.746397, longitude=37.634369)
        ))))
    except Exception:
        print(sys.exc_info()[0], sys.exc_info()[1])

