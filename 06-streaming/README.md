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

![image](https://github.com/user-attachments/assets/20424d9d-19f2-400b-befc-bb2fd8e60125)

![image](https://github.com/user-attachments/assets/61468cc9-0d9f-4fe7-9824-b04cdfa69f06)

6.8-Kafka stream join

![image](https://github.com/user-attachments/assets/829ff6be-f646-4a33-b7ec-d03bef65cea5)

6.9-Kafka stream testing

6.10-Kafka stream windowing

shuffling in a distribute system is costly, a global k table instead of a k table, the complete data is avaliable to each node.

Cause the whole table is stored in the node itself, there might be a memory issue or size issue.

So data like post code would more likely be stored in global k table

![image](https://github.com/user-attachments/assets/298cd777-71d3-4833-8b55-5534a35cf81a)

![image](https://github.com/user-attachments/assets/a6425fea-d2f4-49a8-b8c9-8fe109446bbc)

![image](https://github.com/user-attachments/assets/54a49666-7e5a-419c-9d07-89d5629eaf66)

![image](https://github.com/user-attachments/assets/14f06511-4bdb-43f8-8feb-d42785dd62e5)

![image](https://github.com/user-attachments/assets/1dbe6f8b-9b96-4c45-8c85-ad2238bbc611)

![image](https://github.com/user-attachments/assets/ebc61ea1-67bf-49ac-ac43-f15137d1617b)

![image](https://github.com/user-attachments/assets/44d75f30-f680-47d4-84ea-030a3dd38ed0)

![image](https://github.com/user-attachments/assets/0500ab17-ca46-4825-85f4-5aa9da2e1b56)

6.11-Kafka ksqldb & Connect

6.12-Kafka Schema registry
![image](https://github.com/user-attachments/assets/cdc05293-46ba-4c43-9c0b-dba1721853c4)

![image](https://github.com/user-attachments/assets/a47409e3-f42a-4a82-a1b1-7e4a08342d36)
![image](https://github.com/user-attachments/assets/8135ccd3-acb0-40be-9584-b7ac93809137)
