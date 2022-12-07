import sys
import requests
import config
from typing import NamedTuple


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


class Address(NamedTuple):
    city_for_geocoder: str
    street_for_geocoder: str
    house_for_geocoder: str


def parse_coordination(response_geocoder_output: dict) -> Coordinates:
    return Coordinates(
        latitude=response_geocoder_output['result']['items'][0]['point']['lat'],
        longitude=response_geocoder_output['result']['items'][0]['point']['lon'])


def get_response_geocoder(address: Address) -> dict:
    url = config.GEOCODER_URL.format(
        city_for_geocoder=address.city_for_geocoder,
        street_for_geocoder=address.street_for_geocoder,
        house_for_geocoder=address.house_for_geocoder
    )
    return requests.get(url).json()


if __name__ == "__main__":
    try:
        print(parse_coordination((get_response_geocoder(Address(
            city_for_geocoder='Санкт-Петербург',
            street_for_geocoder='Набережная мойки',
            house_for_geocoder=14
        )))))
    except Exception:
        print(sys.exc_info()[0], sys.exc_info()[1])



