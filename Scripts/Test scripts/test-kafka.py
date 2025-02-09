# -*- coding: utf-8 -*-

from kafka import KafkaProducer
import json
import time

# Configuration du producteur
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],  # Adresse du broker Kafka
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Sérialisation JSON
)

topic = "interaction"  # Nom du topic

# Envoi de messages
for i in range(100):
    message = {"wiiii": i, "message": ("message content is "+str(i))}
    producer.send(topic, value=message)
    print(f"Message envoyé : {message}")
    time.sleep(3)  # Pause pour simuler des envois réguliers

producer.close()
