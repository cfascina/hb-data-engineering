import boto3
import json
import time

from datetime import datetime
from faker import Faker

client = boto3.client('sns')
faker = Faker()

def get_data():
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


while True:
    data = get_data()
    client.publish(
        TopicArn = 'arn:aws:sns:us-east-1:911739205087:consumer-created',
        Message = json.dumps(data)
    )

    print(data)
    time.sleep(1)
