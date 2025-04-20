# producer.py
from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    data = {
        'sensor_id': random.randint(1, 5),
        'temperature': round(random.uniform(20.0, 30.0), 2),
        'timestamp': int(time.time())
    }
    producer.send('sensor-data', value=data)
    time.sleep(1)
