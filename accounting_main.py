import sys
from typing import NamedTuple

import psycopg2
from loguru import logger

from api_distance_matrix_service import get_distance_between_coordinates
from api_geocoder_service import Address, get_coordinates
from config import host, user, password, db_name

logger.add("log.log", format="{time} {level} {message}",
           level="DEBUG", rotation="10 MB", compression="zip")


class SourceTripData(NamedTuple):
    date_of_trip: str
    auto_number: str
    city_departure: str
    street_departure: str
    house_departure: str
    city_arrival: str
    street_arrival: str
    house_arrival: str


class TripDataIntoDB(NamedTuple):
    date_of_trip: str
    auto_number: str
    city_departure: str
    street_departure: str
    house_departure: str
    city_arrival: str
    street_arrival: str
    house_arrival: str
    km_trip: float
    consumption_of_petrol_trip: float


@logger.catch
def main():
    with psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
    ) as connection:
        connection.autocommit = True

        with connection.cursor() as cursor:
            send_data_into_db(cursor)


def send_data_into_db(cursor: psycopg2.extensions.cursor) -> None:
    trip_data_for_db = get_trip_data_for_sent_into_db()

    cursor.execute("SELECT id FROM auto WHERE number = %(auto_number)s",
                   {'auto_number': trip_data_for_db.auto_number})
    id_auto = cursor.fetchone()
    args_for_command_into_trip = {
        'date_of_trip': trip_data_for_db.date_of_trip,
        'id_auto': id_auto,
        'city_departure': trip_data_for_db.city_departure,
        'street_departure': trip_data_for_db.street_departure,
        'house_departure': trip_data_for_db.house_departure,
        'city_arrival': trip_data_for_db.city_arrival,
        'street_arrival': trip_data_for_db.street_arrival,
        'house_arrival': trip_data_for_db.house_arrival,
        'km_trip': trip_data_for_db.km_trip,
        'consumption_of_petrol_trip': trip_data_for_db.consumption_of_petrol_trip
    }
    cursor.execute("""
        INSERT into trip(
            date,
            number_id,
            city_departure,
            street_departure,
            house_departure,
            city_arrival,
            street_arrival,
            house_arrival,
            km_trip,
            consumption_of_petrol
        )
        VALUES (
            %(date_of_trip)s,
            %(id_auto)s,
            %(city_departure)s,
            %(street_departure)s,
            %(house_departure)s,
            %(city_arrival)s,
            %(street_arrival)s,
            %(house_arrival)s,
            %(km_trip)s,
            %(consumption_of_petrol_trip)s
        );
    """, args_for_command_into_trip)

    logger.info(f'\nTrip data({trip_data_for_db.date_of_trip}) has been send to the database.\n'
                f'Auto number - {trip_data_for_db.auto_number}, distance - {trip_data_for_db.km_trip} km.')


def get_trip_data_for_sent_into_db() -> TripDataIntoDB:
    source_data = get_source_trip_data()

    point_departure = Address(
        source_data.city_departure,
        source_data.street_departure,
        source_data.house_departure
    )
    point_arrival = Address(
        source_data.city_arrival,
        source_data.street_arrival,
        source_data.house_arrival
    )

    coordinates_departure = get_coordinates(point_departure)
    coordinates_arrival = get_coordinates(point_arrival)
    km_trip = get_distance_between_coordinates(coordinates_departure,
                                               coordinates_arrival)
    consumption_of_petrol_trip = round((km_trip * 7.4 / 100), 2)

    return TripDataIntoDB(
        date_of_trip=source_data.date_of_trip,
        auto_number=source_data.auto_number,
        city_departure=source_data.city_departure,
        street_departure=source_data.street_departure,
        house_departure=source_data.house_departure,
        city_arrival=source_data.city_arrival,
        street_arrival=source_data.street_arrival,
        house_arrival=source_data.house_arrival,
        km_trip=km_trip,
        consumption_of_petrol_trip=consumption_of_petrol_trip)


def get_source_trip_data() -> SourceTripData:
    # TODO: add validation
    date_of_trip = input('Введите дату в формате "2022-09-30": ')
    auto_number = input('Введите гос.номер автомобиля в формате "a000aa99": ')

    city_departure = (input('Введите город (отправление): ')).title()
    street_departure = (input('Введите улицу (отправление): ')).title()
    house_departure = input('Введите номер дома (отправление): ')

    city_arrival = (input('Введите город (назначение): ')).title()
    street_arrival = (input('Введите улицу (назначение): ')).title()
    house_arrival = input('Введите номер дома (назначение): ')

    return SourceTripData(
        date_of_trip=date_of_trip,
        auto_number=auto_number,
        city_departure=city_departure,
        street_departure=street_departure,
        house_departure=house_departure,
        city_arrival=city_arrival,
        street_arrival=street_arrival,
        house_arrival=house_arrival
    )


if __name__ == "__main__":
    try:
        main()
    except (Exception, psycopg2.DatabaseError):
        print(sys.exc_info()[0], sys.exc_info()[1])
    except KeyboardInterrupt:
        logger.error("KeyboardInterrupt")
        print('\nRun the program again')
