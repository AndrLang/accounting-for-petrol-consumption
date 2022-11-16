from api_geocoder_service import get_response_geocoder, parse_coordination, \
    Address
from api_distance_matrix_service import get_response_distance_matrix, \
    parse_distance, get_distance_kilometer
from typing import NamedTuple


class DataIntoDB(NamedTuple):
    auto_number: str
    date: str
    city_departure: str
    street_departure: str
    house_departure: str
    city_arrival: str
    street_arrival: str
    house_arrival: str
    km_trip: float
    consumption_of_petrol_trip: float


def get_data() -> DataIntoDB:
    data = input('Введите дату в формате "2022-09-30": ')
    auto_number = input('Введите гос.номер автомобиля в формате "a000aa99": ')

    city_departure = input('Введите город (отправление): ')
    street_departure = input('Введите улицу (отправление): ')
    house_departure = input('Введите номер дома (отправление): ')

    city_arrival = input('Введите город (назначение): ')
    street_arrival = input('Введите улицу (назначение): ')
    house_arrival = input('Введите номер дома (назначение): ')

    point_departure = Address(city_departure, street_departure, house_departure)
    point_arrival = Address(city_arrival, street_arrival, house_arrival)
    coordinates_departure = parse_coordination(get_response_geocoder(point_departure))
    coordinates_arrival = parse_coordination(get_response_geocoder(point_arrival))

    km_trip = get_distance_kilometer(parse_distance(get_response_distance_matrix(
        coordinates_departure,
        coordinates_arrival
    )))
    consumption_of_petrol_trip = round((km_trip * 7.4 / 100), 2)
    return DataIntoDB(
        date=data,
        auto_number=auto_number,
        city_departure=city_departure,
        street_departure=street_departure,
        house_departure=house_departure,
        city_arrival=city_arrival,
        street_arrival=street_arrival,
        house_arrival=house_arrival,
        km_trip=km_trip,
        consumption_of_petrol_trip=consumption_of_petrol_trip
    )


def main():
    data = get_data()
    print(data)
    print(list(data))


if __name__ == "__main__":
    main()
