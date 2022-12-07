from api_geocoder_service import get_response_geocoder, parse_coordination, \
    Address
from api_distance_matrix_service import get_response_distance_matrix, \
    parse_distance, get_distance_kilometer
from typing import NamedTuple
from config import host, user, password, db_name
import psycopg2
import sys


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


def main():
    send_data_into_db(get_trip_data_to_sent_into_db(get_source_trip_data()))


def send_data_into_db(trip_data: TripDataIntoDB) -> None:
    command_get_id_auto = "SELECT id FROM auto WHERE number = %(auto_number)s"

    connection = None
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    cursor.execute(command_get_id_auto, {'auto_number': trip_data.auto_number})
    number_id_into_db = cursor.fetchone()

    agr_for_command_into_trip = [
        trip_data.date_of_trip,
        number_id_into_db,
        trip_data.city_departure,
        trip_data.street_departure,
        trip_data.house_departure,
        trip_data.city_arrival,
        trip_data.street_arrival,
        trip_data.house_arrival,
        trip_data.km_trip,
        trip_data.consumption_of_petrol_trip
    ]
    command_into_trip = (
        """
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
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    )
    cursor.execute(command_into_trip, agr_for_command_into_trip)
    cursor.close()
    connection.commit()
    if connection:
        connection.close()
        print('[INFO] PostgreSQL connection closed')


def get_trip_data_to_sent_into_db(source_data: SourceTripData) -> TripDataIntoDB:
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
    coordinates_departure = parse_coordination(get_response_geocoder(point_departure))
    coordinates_arrival = parse_coordination(get_response_geocoder(point_arrival))

    km_trip = get_distance_kilometer(parse_distance(get_response_distance_matrix(
        coordinates_departure,
        coordinates_arrival
    )))
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
        print('Run the program again')
    else:
        print('Trip data has been send to the database')



