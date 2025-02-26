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


## 6.4-Confluent cloud

## 6.5-Kafka producer consumer

## 6.6-Kafka configuration

What is a Kafka Cluster

different machine/nodes running together (zookeeper not there any more)

![image](https://github.com/user-attachments/assets/89038143-e77e-4fff-9cc8-6c3d20de398c)

How Kafka provides reliability

![image](https://github.com/user-attachments/assets/105cbc41-f48b-45bc-b9e4-e7cc3707de9f)

Retention-how long the data will be retained by Kafka

![image](https://github.com/user-attachments/assets/6486c8df-38a1-408c-bfbc-6917d2719ab6)

![image](https://github.com/user-attachments/assets/7378ea6b-10c3-4d25-a922-ab0a98159798)


Partitions--what allows Kafka to scale

![image](https://github.com/user-attachments/assets/6348dc97-a50c-4247-aec4-54730a69d81c)

offset-which message to consume

![image](https://github.com/user-attachments/assets/a299a0a6-0323-469d-ad2e-a528cd6d05f4)

When a new consumer connect, the auto offset it gonna define how it reads the message.
![image](https://github.com/user-attachments/assets/6f8cbd6d-4dd6-4a2c-8c83-4196c5c8b32d)


Acknowledgment all

![image](https://github.com/user-attachments/assets/09ae5544-54a3-4c17-8ae1-4dbd0f090f5c)

https://kafka.apache.org/20/documentation.html


6.7-Kafka streams basics




