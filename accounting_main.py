from api_geocoder_service import get_response_geocoder, parse_coordination, \
    Address, Coordinates
from api_distance_matrix_service import get_response_distance_matrix, \
    parse_distance, get_distance_kilometer


def main():
    city_source = input('Введите город (отправление): ')
    street_source = input('Введите улицу (отправление): ')
    house_source = input('Введите номер дома (отправление): ')

    city_target = input('Введите город (назначение): ')
    street_target = input('Введите улицу (назначение): ')
    house_target = input('Введите номер дома (назначение): ')

    point_source = Address(city_source, street_source, house_source)
    point_target = Address(city_target, street_target, house_target)
    coordinates_source = parse_coordination(get_response_geocoder(point_source))
    coordinates_target = parse_coordination(get_response_geocoder(point_target))

    total_km = get_distance_kilometer(parse_distance(get_response_distance_matrix(
        coordinates_source,
        coordinates_target
    )))
    print(total_km)


if __name__ == "__main__":
    main()
