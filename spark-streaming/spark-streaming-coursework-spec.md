CSC8101 Spark Streaming Coursework
=====================================

Introduction
------------

Web sites often try to provide content recommendations based on user activity. 
This may be aggregate, as in 'most watched movies', 'bestsellers', or it may be 
personalized to varying degrees, as with 'more items like these' or 'customers 
like you also watched'.

The architecture of such applications includes a means to capture relevant 
events, such as which pages/items the users are viewing; a model to segment or 
group the events and/or users; a model to calculate predictions and a dynamic 
content delivery engine to personalise the site for the user based on the 
output of the model.

In this coursework you'll implement some of the pieces of such an application:
namely the system that receives the raw event streams (page view information
for clients), aggregates the data and issues it to the database layer for 
storage.

You will build on the experience you gained with [Spark](http://spark.apache.org/) 
in the previous coursework. However, instead of static data, this assignment 
deals with real-time streaming data arriving from a message broker, in this 
case [Apache Kafka](http://kafka.apache.org/).

### Spark Streaming

Spark's Streaming module allows you to apply the power of Spark's distributed 
and resilient processing system to real time data streams. Spark Streaming is 
a layer on top of Spark's core libraries and allows incoming data to be grouped 
into small batches, each of which is treated as an individual RDD.

![streaming flow](img/streaming-flow.png)

![dstream flow](img/streaming-dstream.png)

It should be noted that the stream of RDDs (referred to as a DStream) has a 
different set of available operations to that of standard RDDs. It is __strongly__ 
recommended that your read the [Spark Streaming Programming Guide](http://
spark.apache.org/docs/latest/streaming-programming-guide.html) on the Spark 
website to understand the difference from the core Spark libraries and the 
constraints that stream processing introduces. 

![dstream operations](img/streaming-dstream-ops.png)

The programming guide has examples in several languages (Scala, Java and Python) 
and details all the available operations for DStreams. Additional language 
specific implementation details can be found in the appropriate 
[API documentation](http://spark.apache.org/docs/latest/api/).

### Kafka

[Apache Kakfa](http://kafka.apache.org/) is a distributed, partitioned, 
replicated commit log service. It has many [uses](http://
kafka.apache.org/documentation.html#uses), however for this assignment we will 
be using it as a [message broker](https://en.wikipedia.org/wiki/Message_broker) 
that can store incoming messages from a variety of sources (often called 
producers) and serve these to multiple consumers.

Message brokers are often employed to serve as an intermediary between the 
different layers of a software application stack. They can simplify large 
distributed computing systems by separating different layers from one another. 
For example, say you had a large number of sensors deployed around a city, that 
are reporting to a cluster of computers that process the sensor information. 
If in the future you change the location of the cluster, you would have to 
inform all the sensors (potentially many thousands of them) of the change of 
receiving address. Similarly, if you switch your cluster to a new software 
system or communication protocol, you would also have to update all of 
your sensors to use this new system. Placing a message broker between the 
sensors and the processing infrastructure solves these two issues. The sensors 
always send to the broker and do not need to be informed of the processing 
system or its protocols and visa versa.

Message brokers also act as buffers to smooth out spikes in traffic and are 
often employed in big data processing systems for this purpose. For this 
assignment you will be connecting to a Kafka broker located in the AWS cloud.

Knowing the internal operations of Kafka are not required for this assignment, 
however reading the [introduction](http://kafka.apache.org/
documentation.html#introduction) on the Kafka website will give you an 
understanding of the terms used in the connection API and may help in 
understanding error messages produced by your Spark code in relation to Kafka.

Links
-----

* [CSC8101 module site](https://sites.google.com/site/paolomissier/home/for-students/csc8101-big-data-analytics)
* [Spark Streaming Programming Guide](http://spark.apache.org/docs/latest/streaming-programming-guide.html)
* [Spark + Kafka Guide](https://spark.apache.org/docs/latest/streaming-kafka-0-8-integration.html)

Developing Spark Streaming Programs
-----------------------------------

So far you have been developing Spark batch jobs that run once and stop 
processing when they reach the end of the input source. This lends itself 
towards the Jupyter notebook style of running a command and seeing the output, 
changing parameters and running the code again. 

However, Spark Streaming is different. The program you define will run 
continuously and will not stop unless it encounters an error. This can result
in large amounts of input being printed in the notebook and the only way to 
stop you program is to kill it manually. This can lead to issues with notebook
kernels crashing and you may find you have to restart often.

Therefore it recommended that for this coursework you write standard `.py` files
and use the `spark-submit` program to run them locally on your VM. A stub python
file has been [provided](https://raw.githubusercontent.com/tomncooper/CSC8101-Documentation/master/spark-streaming/stub.py), this defines the spark context and streaming context
objects and has additional helper methods for some of the database connection 
tasks. You should use this file as a base, make a copy of it for your project 
and add your code to complete the tasks below. 

To get the stub file either clone the documentation repository and navigate to
the `spark-streaming` folder:

`$ git clone https://github.com/tomncooper/CSC8101-Documentation.git` 

Or you can simply download the stub directly using `wget`:

`$ wget https://raw.githubusercontent.com/tomncooper/CSC8101-Documentation/master/spark-streaming/stub.py`

### Running streaming jobs locally

In order for the stub code to work correctly and for you to have access to the 
Kafka and Cassandra connection APIs, you will need to tell spark to download 
some additional dependencies when it runs your programs. Run the command below 
on your VM to execute your program:

`$ spark-submit --packages com.datastax.spark:spark-cassandra-connector_2.11:2.0.0-M3,org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.0 your_streaming_program.py`  

### Running streaming jobs on the cluster

To run your job on the spark cluster, change the master argument supplied to
the SparkContext object from `master="Local[2]"` to `master="CLUSTER_IP"`. You 
will also need set the Cassandra address key in the SparkConf object to point 
at your VM's IP address.

### Hints

* If you are developing using standard `py` files and `spark-submit` you will 
often want to see what is inside your DStreams at various stages. A simple way 
to do this is use the `dstream.pprint(n)` method. At each processing interval 
it will print out the first `n` lines of the RDD for that interval (it is the 
DStream equivalent of running `print(rdd.take(n))` on a Spark Batch rdd). 
* Spark produces a lot of console output by default. Please refer to the 
[FAQ](spark-faq.md) for details of how to reduce or disable this output.

Tasks
-----

In the [Cassandra Coursework](../cassandra/cassandra-coursework-spec.md) you 
created several tables within the Cassandra database on your VM. These were 
designed to receive information from an upstream system. The aim of this 
coursework is to produce this upstream system and take the raw incoming messages 
from a Kafka broker and transform them into the format you database layer now 
expects.

As stated in the earlier coursework specification, the log analysis system you 
are working on receives [JSON](http://www.json.org/) formatted messages from 
multiple web servers in the following form:

```
{"client_id" : "4149719179064208", 
 "timestamp" : "2017-01-25T14:03:32", 
 "url" : {"topic" : "Action", 
          "page" : "Die Hard"}}
```

You are required to design a Spark streaming program that connects to a Kafka
broker, receives the raw event messages and performs the following tasks:

### Task 1: Connect to the Kafka Broker

You have been provided with a [stub](developingsparkstreamingprograms) python 
project which contains the connection code and creates a DStream of raw JSON 
string RDDs, one for every batch interval. You will need to provide the broker 
connection address for the broker you which to pull messages from and the topic
you wish to connect too. The arguments that need changing are highlighted in 
the stub file.

#### Broker Addresses

There are 3 Kafka brokers available on AWS. You have been assigned a broker 
against your student number on 
[this page](https://docs.google.com/spreadsheets/d/1-2XmHUQtStsei2avneCOp8c5RiO3FIBj_EZx11kDf7Q/edit?usp=sharing). Please ensure you connect to the appropriate broker.

#### Topics

On each broker there are two topics.

##### dev-stream

This is low frequency stream roughly 4 events a seconds. It has a dramatically
reduced pool of Client IDs and Topic/Page options. This should be use for your
local development and should yield multiple page hits for each Client ID.

##### production

This is high velocity stream and should only be used when you are confident your 
code is functioning correctly. It has several hundred messages each second and 
depending on your batch/window/slide interval choices may overwhelm your VM. It
is intended that this stream be consumed by jobs running on the spark cluster.

### Task 2: Window the incoming events

The messages will arrive from the Kafka broker as fast as Spark can request 
them. Spark streaming will batch the incoming events into time chunks defined
by the batch interval arguments given to the Spark Streaming Context object.

![streaming flow](img/streaming-flow.png)

Each of these batches forms an RDD in the DStream. It is usually a good idea
to have as short a batch interval as your cluster resources will allow (the 
shorter the interval the more often batches will be processed - adding load 
onto the cluster). More granular RDDs generally allow for faster error recovery,
however you may not want to run complicated transformations for every batch 
interval. Therefore Spark allows you to combine multiple batch interval RDDs 
into a longer window RDD within the DStream.

![windowed stream](img/streaming-dstream-window.png)

You should read through the 
[documentation](https://spark.apache.org/docs/latest/streaming-programming-guide.html#window-operations) 
on windowing operations. You should then create a DStream that contains 2 mins
of events, updated every 1 mins. You can experiment with different batch 
intervals, however these should be much shorter than the window length.

### Task 3: Convert the JSON String into a dictionary/map

Once you have a windowed DStream you should convert the raw JSON strings into 
a dictionary, by creating a conversion function and mapping over the windowed 
raw message DStream. You should consult your chosen language's JSON parsing 
documentation on how to achieve this.

### Task 4: Find the smallest timestamp in each window

As stated in the [Cassandra Coursework](../cassandra/cassandra-coursework-spec.md)
every one of the entries in each batch passed to the database layer will have 
the same timestamp value. This timestamp corresponds to the start of the time 
period that the batch of entries covers. 

Every event message that comes from the broker into Spark Streaming has its own 
timestamp corresponding to the moment it was created. You need to write code to 
find the smallest timestamp within each window period (ie for each RDD in the 
windowed DStream). What you should end up with is a seperate DStream where each 
RDD within the DStream contains a single timestamp, the minimum for each period. 

Later you will apply this timestamp to all of your entries before submitting 
them to the database.

#### Hints

* The timestamps in the raw message streams are in string format. The database
is expecting a unix timestamp (number of milliseconds since 01/01/1970). You
will need to convert the timestamp strings for input into the database. Also 
converting them into integers will simplify finding the smallest value.
* You **should not** collect all the timestamps to the driver to find the smallest
value (there could be hundreds of thousands of them across the cluster). If you 
cannot find a DStream based way to calculate the smallest value then you can 
still use all the RDD based operations on each RDD within the DStream by using
the `dstream.transform()` method. This method takes a function to be applied to
each RDD. The function you supply to `transform()` should accept an RDD and 
**return** an RDD. 

### Task 5: Client visits per URL

In Task 1 of the [Cassandra Coursework](../cassandra/cassandra-coursework-spec.md) 
you were asked to design a table to store the pages visited by each client (and 
how many times they had visited them) in each time period. You now need to write 
the code to create these entries. 

You need to create a DStream, where each RDD contains rows with a Client ID, a 
batch time period timestamp, a Topic, Page and visit count for that page. 

You will need to transform the windowed message stream to collect together 
entries for each Client ID and topic with lists of pages for each. You can then
count the occurrence of each page string to produce the final count DStream.

Once you have your data in the format you want you need to send this to 
the Cassandra tables you prepared for Task 1 of the Cassandra Coursework. The 
stub file you have been provided with, has example code for sending your final 
prepared DStreams to Cassandra. You will need to convert each entry to a Row 
and then convert the RDD to a DataFrame (the conversion code is provided for 
you).

#### Hints

* You need to add the minimum window timestamp you calculated earlier to each
entry in the final count DStream. There are several ways to achieve this, one
way is to give the min timestamp and every entry in the final DStream a common
key and then join them together, cleaning up the combined DSstream into a form
ready for entry into Cassandra.

### Task 6: URL distinct user counts

In Task 2 of the [Cassandra Coursework](../cassandra/cassandra-coursework-spec.md)
you were required to design a table schema to store the number of unique clients
visiting each Topic and Page per time period. You now need to write the code to 
create these entries. 

You need to create a DStream which contains entries consisting of the batch 
timestamp, Topic, Page and the unique visit counts.

To do this your will need to collect the Client IDs visiting each topic and page
combination. You then need to convert the list of client ids (which will contain
duplicates) into a set of unique ids and then count them. There are various ways
to achieve this final unique count. We are looking for ways that take advantage
of Sparks distributed nature, so you should avoid methods that collect lists
back to the diver.

#### Hints

* As with the minimum window timestamp you may need to use RDD functions as well
as the function provided by the DStream. `dstream.transform()` will allow you to 
apply functions to each RDD within a DStream.
* Functions like `rdd.aggregate` and `rdd.combineByKey` can be used to create
custom functions to combine elements of an RDD.
 
### Task 7: Recommend URLs for a User

If you have provided the correct information to your Cassandra tables, then the
program you wrote for Task 3 of the Cassandra Coursework should work correctly
with the data now provided by Spark Streaming. 

You should test your program to ensure it still produces the expected results.
Your program should not be part of your Spark code and should be run, as in the
Cassandra coursework, as a stand alone command line program on your VM that 
simply talks to your local Cassandra instance.
