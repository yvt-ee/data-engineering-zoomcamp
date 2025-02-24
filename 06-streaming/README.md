# Module 6: Stream Processing

What is kafka
Basic components
Avro and Schema Registry
Kafka Connect
Kafka Streams
What questions to ask?

## 6.0.1 Introduction

## 6.0.2-What is stream processing

computer comnication: rest, graph, webhooks

data exchange happening over computer comnication services

Producer(sharing information) kafka topic/spark topic consumer(subscriber who recive the message)

Consumers: kafka, soark, stream processing, BigData

stream: kafka topic/spark topic

real time: a few seconds of delay

![image](https://github.com/user-attachments/assets/2c8d5cd3-95e0-4b51-b647-4ceb8e8255e5)

![image](https://github.com/user-attachments/assets/ecd1a0ee-a235-4bcd-8ac0-3e00e10e8837)

## 6.3-What is kafka?

topic is contunuous tream of events, eg: the temprature of this room in this particular time stamp

log is the way we store events in a topic. each event contains a message, a message includes key, 
value and timestamp can have different properties and certain required fileds and not required fileds.

![image](https://github.com/user-attachments/assets/33b31911-d365-425d-bf6c-ce1a83457267)


kafka provide robustness and reliability to the topic, which called replication, 
it can maintain data in the case the server went down

Scability, can handel data size increases from 10 events per seconds to 1000 events per seconds.

add a lot flexibility.

store data in tier storage.

![image](https://github.com/user-attachments/assets/d93e2f64-83b8-457d-b223-82ac1e881584)

CDC change data capture

monolith

![image](https://github.com/user-attachments/assets/3ea09924-2050-42d2-be92-a5ea0e7f3a95)

![image](https://github.com/user-attachments/assets/fac7b337-9ebc-42f6-a3f7-48a9a213f278)





