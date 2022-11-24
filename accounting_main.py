from api_geocoder_service import get_response_geocoder, parse_coordination, \
    Address
from api_distance_matrix_service import get_response_distance_matrix, \
    parse_distance, get_distance_kilometer
from typing import NamedTuple
from config import host, user, password, db_name
import psycopg2


class SourceTripData(NamedTuple):
    data: str
    auto_number: str
    city_departure: str
    street_departure: str
    house_departure: str
    city_arrival: str
    street_arrival: str
    house_arrival: str


class TripDataIntoDB(NamedTuple):
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


def get_source_trip_data() -> SourceTripData:
    data = input('Введите дату в формате "2022-09-30": ')
    auto_number = input('Введите гос.номер автомобиля в формате "a000aa99": ')

    city_departure = input('Введите город (отправление): ')
    street_departure = input('Введите улицу (отправление): ')
    house_departure = input('Введите номер дома (отправление): ')

    city_arrival = input('Введите город (назначение): ')
    street_arrival = input('Введите улицу (назначение): ')
    house_arrival = input('Введите номер дома (назначение): ')

    return SourceTripData(
        data=data,
        auto_number=auto_number,
        city_departure=city_departure,
        street_departure=street_departure,
        house_departure=house_departure,
        city_arrival=city_arrival,
        street_arrival=street_arrival,
        house_arrival=house_arrival
    )


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
        date=source_data.data,
        auto_number=source_data.auto_number,
        city_departure=source_data.city_departure,
        street_departure=source_data.street_departure,
        house_departure=source_data.house_departure,
        city_arrival=source_data.city_arrival,
        street_arrival=source_data.street_arrival,
        house_arrival=source_data.house_arrival,
        km_trip=km_trip,
        consumption_of_petrol_trip=consumption_of_petrol_trip)


def send_data_into_db(trip_data: TripDataIntoDB) -> None:
    data_trip = list(trip_data)
    print(data_trip)
    command_get_id_auto = "SELECT id FROM auto WHERE number = (%s)"
    command_get_id_city = "SELECT id FROM city WHERE name = (%s)"
    command_get_id_street = "SELECT id FROM street WHERE name = (%s)"
    command_get_id_house = "SELECT id FROM house WHERE number = (%s)"

    #
    # index_del_in_list_main = {0, 1, 8, 9}
    # list_arguments_for_table_route = \
    #     [x for i, x in enumerate(data_trip) if i not in index_del_in_list_main]
    # print(list_arguments_for_table_route)
    #
    # command_into_route = (
    #     """
    #     INSERT into route(
    #         city_departure_id,
    #         street_departure_id,
    #         house_departure_id,
    #         city_arrival_id,
    #         street_arrival_id,
    #         house_arrival_id,
    #         km_between
    #     )
    #     VALUES (%s, %s, %s, %s, %s, %s, %s)""", list_arguments_for_table_route)
    # command_into_route = (
    #     """
    #     INSERT into route(
    #         city_departure_id,
    #         street_departure_id,
    #         house_departure_id,
    #         city_arrival_id,
    #         street_arrival_id,
    #         house_arrival_id,
    #         km_between
    #     )
    #         VALUES (%s, %s, %s, %s, %s, %s, %s)""", list_arguments_for_table_route)
    connection = None
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        cursor = connection.cursor()

        cursor.execute(command_get_id_auto, (data_trip[0],))
        number_id_into_db = cursor.fetchone()
        print(number_id_into_db)

        cursor.execute(command_get_id_city, (data_trip[2],))
        city_id_departure = cursor.fetchone()
        print(city_id_departure)
        cursor.execute(command_get_id_street, (data_trip[3],))
        street_id_departure = cursor.fetchone()
        print(street_id_departure)
        cursor.execute(command_get_id_house, (data_trip[4],))
        house_id_departure = cursor.fetchone()
        print(house_id_departure)

        cursor.execute(command_get_id_city, (data_trip[5],))
        city_id_arrival = cursor.fetchone()
        print(city_id_arrival)
        cursor.execute(command_get_id_street, (data_trip[6],))
        street_id_arrival = cursor.fetchone()
        print(street_id_arrival)
        cursor.execute(command_get_id_house, (data_trip[7],))
        house_id_arrival = cursor.fetchone()
        print(house_id_arrival)
        agr_for_command_into_trip = [
            data_trip[1],
            number_id_into_db,
            city_id_departure,
            street_id_departure,
            house_id_departure,
            city_id_arrival,
            street_id_arrival,
            house_id_arrival,
            data_trip[7],
            data_trip[8]
        ]
        command_into_trip = (
            """
                INSERT into trip(
                    date,
                    number_id,
                    city_departure_id,
                    street_departure_id,
                    house_departure_id,
                    city_arrival_id,
                    street_arrival_id,
                    house_arrival_id,
                    km_total,
                    consumption_of_petrol
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        )

        cursor.execute(command_into_trip, agr_for_command_into_trip)
        cursor.close()
        connection.commit()

        # cursor.execute(command_into_route)
        # cursor.close()
        # connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')


def main():
    data = send_data_into_db(get_trip_data_to_sent_into_db(get_source_trip_data()))
    # print(data)
    # print(list(data))


if __name__ == "__main__":
    main()
