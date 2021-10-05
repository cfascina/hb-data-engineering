from datetime import datetime
from faker import Faker

import psycopg2
import time

faker = Faker(['en_US'])


def get_fake_data():
    lat, lng, city, country, region = faker.location_on_land()
    cur_datetime = datetime.utcnow()

    return dict(
        id = faker.uuid4(),
        name = faker.name(),
        phone = faker.phone_number(),
        email = faker.ascii_free_email(),
        city = city,
        country = country,
        region = region,
        lat = lat,
        lng = lng,
        created_at = f"{cur_datetime}",
        updated_at = f"{cur_datetime}"
    )

def get_query():
    return '''
        INSERT INTO customers VALUES (
            '{id}',
            '{name}',
            '{phone}',
            '{email}',
            '{city}',
            '{country}',
            '{region}',
             {lat},
             {lng},
            '{created_at}',
            '{updated_at}'
        )
    '''.format(**get_fake_data())

dsn = (
    "dbname = {dbname} "
    "user = {user} "
    "password = {password} "
    "port = {port} "
    "host = {host}".format(
        dbname = "myapp",
        user = "postgres",
        password = "admin1234",
        port = "5432",
        host = "myapp.cvrrntmi72bm.us-east-1.rds.amazonaws.com"
    )
)

conn = psycopg2.connect(dsn)
conn.set_session(autocommit = True)

cur = conn.cursor()
cur.execute(
    '''
        CREATE TABLE IF NOT EXISTS customers (
            id uuid PRIMARY KEY,
            name VARCHAR(200),
            phone VARCHAR(200),
            email VARCHAR(200),
            city VARCHAR(200),
            country VARCHAR(200),
            region VARCHAR(200),
            lat FLOAT,
            lng FLOAT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        ) 
    '''
)

for i in range(1, 11):
    query = get_query()
    cur.execute(query)
    time.sleep(1)

conn.close()
