from kafka import KafkaProducer
import json
import time
import random

# Configurar productor
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = "traffic-data"

cities = ["Bogota", "Medellin", "Cali", "Barranquilla", "Cartagena"]
vehicle_types = ["car", "bus", "moto", "truck"]

print("Enviando datos de tráfico al topic 'traffic-data'...")

while True:
    data = {
        "city": random.choice(cities),
        "vehicle_type": random.choice(vehicle_types),
        "count": random.randint(1, 20),
        "timestamp": time.time()
    }
    producer.send(topic, value=data)
    print(f"Enviado: {data}")
    time.sleep(1)