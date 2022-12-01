import psycopg2
from dotenv import load_dotenv
from config import host, user, password, db_name

load_dotenv()


def create_table():
    commands = (
        """
        CREATE TABLE auto(
            id serial PRIMARY KEY,
            number varchar(255) NOT NULL,
            consumption_per_100km numeric NOT NULL
        )
        """,
        """
        CREATE TABLE trip(
            id serial PRIMARY KEY,
            date date NOT NULL,
            number_id integer references auto(id),
            city_departure varchar(255) NOT NULL,
            street_departure varchar(255) NOT NULL,
            house_departure varchar(255) NOT NULL,
            city_arrival varchar(255) NOT NULL,
            street_arrival varchar(255) NOT NULL,
            house_arrival varchar(255) NOT NULL,
            km_trip numeric NOT NULL,
            consumption_of_petrol numeric NOT NULL
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
