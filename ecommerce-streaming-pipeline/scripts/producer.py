import json
import time
from kafka import KafkaProducer
from data_generator import generate_transaction

KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'ecommerce_transactions'

def create_producer():
    return KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def start_streaming():
    producer = create_producer()
    print(f"Starting to stream to topic: {TOPIC_NAME}")
    try:
        while True:
            transaction = generate_transaction()
            producer.send(TOPIC_NAME, transaction)
            print(f"Sent: {transaction['transaction_id']}")
            time.sleep(0.5) # Simulate 2 events per second
    except KeyboardInterrupt:
        print("Streaming stopped.")
    finally:
        producer.close()

if __name__ == "__main__":
    start_streaming()
