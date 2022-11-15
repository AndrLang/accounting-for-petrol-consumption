import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

host = '127.0.0.1'
user = 'postgres'
password = os.getenv("POSTGRES")
db_name = 'petrol_consumption'


def create_table():
    commands = (
        """
        CREATE TABLE auto(
            id serial PRIMARY KEY,
            number varchar(255) NOT NULL,
            consumption_on_100km numeric NOT NULL
        )
        """,
        """
        CREATE TABLE city(
            id serial PRIMARY KEY,
            name varchar(255) NOT NULL
        )
        """,
        """
        CREATE TABLE street(
            id serial PRIMARY KEY,
            name varchar(255) NOT NULL
        )
        """,
        """
        CREATE TABLE house(
            id serial PRIMARY KEY,
            number varchar(255) NOT NULL
        )  
        """,
        """
        CREATE TABLE trip(
            id serial PRIMARY KEY,
            date date NOT NULL,
            number_id integer references auto(id),
            city_departure_id integer references city(id),
            street_departure_id integer references street(id),
            house_departure_id integer references house(id),
            city_arrival_id integer references city(id),
            street_arrival_id integer references street(id),
            house_arrival_id integer references house(id),
            km_total integer NOT NULL,
            consumption_of_petrol integer NOT NULL
        )
        """,
        """
        CREATE TABLE route(
            id serial PRIMARY KEY,
            city_departure_id integer references city(id),
            street_departure_id integer references street(id),
            house_departure_id integer references house(id),
            city_arrival_id integer references city(id),
            street_arrival_id integer references street(id),
            house_arrival_id integer references house(id),
            km_between integer NOT NULL
        )
        """)
    connection = None
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        cursor = connection.cursor()
        for command in commands:
            cursor.execute(command)
        cursor.close()
        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')


if __name__ == '__main__':
    create_table()
