from datetime import datetime
from faker import Faker

import psycopg2
import time

faker = Faker(['en_US'])


def get_query(cur):
    cur.execute("SELECT id FROM customers ORDER BY RANDOM() LIMIT 1")
    id = cur.fetchone()[0]
    
    return '''
        UPDATE customers SET
            phone = '{phone}', 
            updated_at = '{updated_at}'
        WHERE id = '{id}'
    '''.format(
        phone = faker.phone_number(),
        updated_at = datetime.utcnow(),
        id = id
    )

dsn = (
    "dbname = {dbname} "
    "user = {user} "
    "password = {password} "
    "port = {port} "
    "host = {host}".format(
        dbname = "",
        user = "",
        password = "",
        port = "",
        host = ""
    )
)

conn = psycopg2.connect(dsn)
conn.set_session(autocommit = True)

cur = conn.cursor()

for i in range(1, 11):
    query = get_query(cur)
    cur.execute(query)
    time.sleep(1)

conn.close()
