import sys
import requests
from api_geocoder_service import Coordinates
import config


def get_distance_between_coordinates(coordinates_departure: Coordinates,
                                     coordinates_arrival: Coordinates):
    distance_matrix = get_response_distance_matrix(coordinates_departure,
                                                   coordinates_arrival)
    distance_between_coordinates = parse_distance(distance_matrix)
    return round_distance(distance_between_coordinates)


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


def parse_distance(response_distance_matrix_output: dict) -> int:
    return response_distance_matrix_output["routes"][0]["distance"]


def round_distance(parse_distance_output: int) -> float:
    return round(parse_distance_output / 1000, 2)


if __name__ == "__main__":
    try:
        coordinates_departure = Coordinates(latitude=55.75142, longitude=37.615606)
        coordinates_arrival = Coordinates(latitude=55.746397, longitude=37.634369)
        print(get_distance_between_coordinates(coordinates_departure, coordinates_arrival))
    except Exception:
        print(sys.exc_info()[0], sys.exc_info()[1])
