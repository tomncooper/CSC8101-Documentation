CSC8101 Spark Streaming Coursework
=====================================

Introduction
------------

For this coursework you will use [Apache Spark's streaming](http://
spark.apache.org/streaming/) functionality to process an activity event stream 
and populate the Cassandra tables you designed in the earlier database 
coursework.

### Overview

Web sites often try to provide content recommendations based on user activity. 
This may be aggregate, as in 'most read stories', 'bestsellers', or it may be 
personalized to varying degrees, as with 'more items like these' or 'customers 
like you also read'.

The architecture of such applications includes a means to capture relevant 
events, such as which pages/items the users are viewing; a model to segment or 
group the events and/or users; a model to calculate predictions and a dynamic 
content delivery engine to personalise the site for the user based on the 
output of the ML model.

In this coursework you'll implement some of the pieces of such an application:
namely the system that recieves the raw event streams (page view information
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

\begin{center}
  \includegraphics[height=2.8cm]{img/streaming-flow.png}
\end{center}

It should be noted that the stream of RDDs (refered to as a DStream) has a 
different set of available operations to that of standard RDDs. It is __strongly__ 
recommended that your read the [Spark Streaming Programming Guide](http://
spark.apache.org/docs/latest/streaming-programming-guide.html) on the Spark 
website to understand the difference from the core Spark libraries and the 
constraints that stream processing introduces. The programming guide has 
examples in several languages (Scala, Java and Python) and details all the 
available operations for DStreams. Additional language specific implementation 
details can be found in the appropriate [API documentation](http://
spark.apache.org/docs/latest/api/).

### Kafka

[Apache Kakfa](http://kafka.apache.org/) is a distributed, partitioned, 
replicated commit log service. It has many [uses](http://
kafka.apache.org/documentation.html#uses), however for this assignment we will 
be using it as a [message broker](https://en.wikipedia.org/wiki/Message_broker) 
that can store incoming messages from a variety of sources (often called 
producers) and serve these to multiple consumers.

\begin{center}
  \includegraphics[height=4cm]{img/producer_consumer.png}
\end{center}

Message brokers are often employed to serve as an intermediary between 
different the different layers of a software application stack. They can 
simplify large distributed computing systems by separating different layers 
from one another. For example, say you had a large number of sensors deployed 
around a city, that are reporting to a a cluster of computers that process the 
sensor information. If in the future you change the location of the cluster, 
you would have to inform all the sensors (potentially many hundreds of them) of 
the change of receiving address. Similarly, if you switch your cluster to a new 
software system or communication protocol, you would also have to update all of 
your sensors to use this new system. Placing a message broker between the 
sensors and the processing infrastructure solves these two issues. The sensors 
always send to the broker and do not need to be informed of the processing 
system or its protocols and visa versa.

Message brokers also act as buffers to smooth out spikes in traffic and are 
often employed in big data processing systems for this purpose. Typically, 
brokers are deployed on a cluster of machines in the cloud, however for this 
assignment you will be running a Kafka instance locally on your VM.

Knowing the internal operations of Kafka are not required for this assignment, 
however reading the [introduction](http://kafka.apache.org/
documentation.html#introduction) on the Kafka website will give you an 
understanding of the terms used in the setup scripts supplied on your VM and 
may help in understanding error messages produced by your Spark code in relation 
to Kafka.

Links
-----

* [CSC8101 module site](https://sites.google.com/site/paolomissier/home/
for-students/csc8101-big-data-analytics)
* [CSC8101 Spark Streaming Slides](<insert-link-here>)


Setup
-----

### Submitting spark streaming jobs

### Interactive development with pyspark


Tasks
-----

The log analysis system you are working receives [JSON](http://www.json.org/) 
formatted messages from multiple web servers in the following form:

`{"client_id" : "4149719179064208", "timestamp" : "2017-01-25T14:03:32", 
 "url" : {"topic" : "fiction/crime", "page" : "SherlockHolmes"}}`

For the purposes of the following tasks, you can assume that an upstream system
has extracted the relevant information from these messages (we are not 
expecting you to parse the raw JSON message). Therefore for the insert 
statements required in the task below you can simply provide your own dummy 
data. 

The upstream system will collect messages into batches based on their arrival
time. The timestamp value for all the messages delivered to the database will
be the same for all messages in the same batch and corresponds to the start
time of the collection window for that batch.

You should pay attention to the field names and data types in the original 
messages when forming your table schema, so that your database will be 
compatible with the upstream system. A later coursework will involve creating 
this upstream system so be sure to take care designing your schema as it will 
save you work later on.


### Task 3: Recommend URLs for a User

Yes, we're are approaching these tasks in reverse order. Since Cassandra schema 
design is based on a 'query first' approach, you need to know what queries you 
are going to run before you can do the table design and testing. It is 
recommended that you read through all the tasks __before__ you attempt to write
the solutions.

You are required to design a system to recommend Pages for a given Client ID
and Topic. The proposed process is that you should take the top N Pages for the
given Topic from the most recent time period (batch). From this list you should 
exclude any pages that the Client ID has visited in the last 3 time periods. 
This will require you to use both the tables created in tasks 1 and 2.

To display the results of your query you are required to provide a simple 
program that can be used from the command line. It should accept a Client ID 
string, a Topic string and the value of N (the number of top URLs to use in 
the recommendation) as arguments. It should then return a recommended list of 
Pages.

For the purposes of this task your program can be very simple, you should just
print the recommended URLs to the console. You can use either Python, Java or
Scala to create your program. Links to the relevant Cassandra APIs for each
are listed in the [links](#links) section at the top of this page.

### Task 2: URL distinct user counts

You are required to design a table schema to store the number of unique clients
visiting each Topic and Page per time period.

For each event given to your database, you should assume that the 
upstream system will provide the batch timestamp, Topic and Page as strings. 
The user visit count will be supplied as an integer.
 
Once you have created your table, write a series of CQL statements to insert 
dummy data into the table.

To satisfy task 3, write a CQL query to list the top N Pages ranked by visitor 
count for a given Topic and time period. You can assume that the value of N 
will never be greater than 50.

### Task 1: Client visits per URL

You are required to design a table schema to store the number of visits each
Client ID makes to a given Topic and Page per batch time period.

For each event message supplied to your database, you should assume that the 
upstream system will provide a Client ID string, a batch time period timestamp 
string, a Topic string and a Page string. The visit count for each page will 
be supplied as an integer. 

Once you have created your table, write a series of CQL statements to insert 
dummy data into it.

To satisfy task 3, write a CQL query to list for a given Client ID, Topic and 
batch time period, all the Pages they have visited.

### Deliverables

Submission: Program code to provide the recommendations. Table definition 
statements in CQL. Test data that shows your program functions correctly in a 
variety of circumstances.  

Viva: You may be expected to explain e.g. your table design decisions, how the 
database handles the queries at scale, how you chose your test data.
