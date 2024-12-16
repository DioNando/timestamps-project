from kafka import KafkaConsumer
from pymongo import MongoClient
import json

consumer = KafkaConsumer(
    'timestamps',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

client = MongoClient('mongodb://root:example@mongodb:27017/?authSource=admin')  # Connexion à MongoDB
db = client['timestamp_db']
collection = db['timestamps']

if __name__ == "__main__":
    for message in consumer:
        data = message.value
        data["formatted_date"] = data["timestamp"].replace("T", " ")
        collection.insert_one(data)
        print(f"Consumed and stored: {data}")
