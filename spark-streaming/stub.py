""" CSC8101 Streaming coursework stub file"""

from pyspark import SparkContext, SparkConf, RDD
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import SparkSession, Row

def getSparkSessionInstance(sparkConf: SparkConf) -> SparkSession:
    """ This method ensures that there is only ever one instance of the Spark
    SQL context. This prevents conflicts between executors.

    Code taken from example on this page of the Spark Streaming Guide:

    https://spark.apache.org/docs/latest/
    streaming-programming-guide.html#dataframe-and-sql-operations

    Arguments:
        sparkConf - SparkConf - The spark context configuration object.
        This should be the same as supplied to the StreamingContext object.

    Returns:
        The singleton instance of the Spark SQL SparkSession object.
    """
    if "sparkSessionSingletonInstance" not in globals():
        globals()["sparkSessionSingletonInstance"] = SparkSession \
            .builder \
            .config(conf=sparkConf) \
            .getOrCreate()

    return globals()["sparkSessionSingletonInstance"]

def send_to_cassandra(rdd: RDD, table_name: str) -> None:
    """ Converts an RDD of Row instances into a DataFrame and appends it to
    the supplied table name. The Cassandra database address is defined in the
    "spark.cassandra.connection.host" key set in the SparkConf instance given
    to the getSparkSessionInstance method.

    Arguments:
        rdd - RDD - An rdd of Row instances with filed names that match those
        in the target cassandra table.
        table_name - str - The name of the table that this rdd should be sent
        to.

    """
    # Get the singleton instance of SparkSession
    spark = getSparkSessionInstance(rdd.context.getConf())

    # Convert the supplied rdd of Rows into a dataframe
    rdd_df = spark.createDataFrame(rdd)

    # Print the dataframe to the console for verification
    rdd_df.show()

    # Write this dataframe to the supplied Cassandra table
    (rdd_df.write.format("org.apache.spark.sql.cassandra").mode('append')
     .options(table=table_name, keyspace="csc8101").save())

########## Spark Streaming Setup ##########

# Create a conf object to hold connection information
sp_conf = SparkConf()

# Set the cassandra host address - NOTE: you will have to set this to the
# address of your VM if you run this on the cluster. If you are running
# the streaming job locally on your VM you should set this to "localhost"
sp_conf.set("spark.cassandra.connection.host", "localhost")

# Create the spark context object.
# For local development it is very important to use "local[2]" as Spark
# Streaming needs 2 cores minimum to function properly
SC = SparkContext(master="local[2]", appName="Event Processing", conf=sp_conf)

#Set the batch interval in seconds
BATCH_INTERVAL = 10

#Create the streaming context object
SSC = StreamingContext(SC, BATCH_INTERVAL)

########## Kafka Setup ##########

# Create receiver based stream
# NOTE: Please edit the Broker IP to match your designated broker address.
# Also edit the client_id_for_broker to be something personal to you such as
# your student number. This is used for the broker to identify your client.
# Also edit the topic_name you would like to pull messages from and the number
# of partitions to consume on that topic. For development 1 is fine, for 
# consuming from the production stream a higher number is recommended.
topic_name = "dev-stream"
client_id_for_broker = "Your Student ID"
num_of_partition_to_consume_from = 1
RAW_MESSAGES = KafkaUtils.createStream(SSC,
                                       "<instert-broker-ip-here>:2181",
                                       client_id_for_broker,
                                       {topic_name: num_of_partitions_to_consume_from})

########## Window the incoming batches ##########

########## Convert each message from json into a dictionary ##########

########## Find the minimum timestamp for window ##########

############################## Task 1 ##############################

#### Calculate the page visits for each client id ####

#### Write the Task 1 results to cassandra ####

# Convert each element of the rdd_example rdd into a Row
# NOTE: This is just example code please rename the DStreams and Row fields to
# match those in your Cassandra table
row_rdd_example = rrd_example.map(lambda x: Row(field1=x[0],
                                                field2=x[1],
                                                field3=x[2],
                                                field4=x[3],
                                                field5=x[4]))

# Convert each rdd of Rows in the DStream into a DataFrame and send to Cassandra
row_rdd_example.foreachRDD(lambda rdd: send_to_cassandra(rdd, your_table_name))

############################## Task 2 ##############################

#### Calculate the unique views per page

#### Write the Task 2 results to cassandra ####

# Initiate the stream processing
SSC.start()
SSC.awaitTermination()
