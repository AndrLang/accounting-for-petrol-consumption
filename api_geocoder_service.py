from typing import NamedTuple

import requests
import config


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


class Address(NamedTuple):
    city_for_geocoder: str
    street_for_geocoder: str
    house_for_geocoder: str


def _get_response_geocoder(address: Address) -> dict:
    url = config.GEOCODER_URL.format(
        city_for_geocoder=address.city_for_geocoder,
        street_for_geocoder=address.street_for_geocoder,
        house_for_geocoder=address.house_for_geocoder
    )
    return requests.get(url).json()


def parse_coordination(response_geocoder_output: dict) -> Coordinates:
    return Coordinates(
        latitude=response_geocoder_output['result']['items'][0]['point']['lat'],
        longitude=response_geocoder_output['result']['items'][0]['point']['lon']
    )

# f = Address("Москва", "Садовническая", "19")
# print(_parse_coordination(_get_response_geocoder(f)))
