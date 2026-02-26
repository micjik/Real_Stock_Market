from kafka import kafkaConsumer
import json
import time

# --- Configuration matching the producer ---

consumer = kafkaConsumer(
    'stock-analysis',
    bootstrap_servers = ['localhost:9094'],
    auto_offset_reset = 'earliest',
    enable_auto_commit = True,
    group_id = 'my-consumer-group', # Define a consumer group
    value_deserializer = lambda x:json.loads(x.decode('utf-8')) 
)

print("Starting kafka consumer.waiting for message on topic 'consumer_info'...")

for message in consumer:
    data = message.value

    # print the received data

    print(f" Value (Deserialize): {data}")

consumer.close()
print("kafka consumer closed.")