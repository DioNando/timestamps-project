from kafka import KafkaProducer
import json
import datetime
import time

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

if __name__ == "__main__":
    while True:
        now = datetime.datetime.now().isoformat()
        message = {"timestamp": now}
        producer.send('timestamps', message)
        print(f"Produced: {message}")
        time.sleep(1)  # Simule une requête chaque seconde
