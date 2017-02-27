# Spark and Neo4j example

Ready to test your coursework solution outside of iPython notebooks? Keep on reading...

## Running in local machine

iPython notebook is an excellent place for data exploration or testing algorithms on smaller datasets, but once you need the power of clouds, you have to take another step further.

### Local Deployment

A [sample program](https://raw.githubusercontent.com/tomncooper/CSC8101-Documentation/master/spark/python-stub/SparkNeo4jSample.py) has been prepared for you to get you started.

This program does two things. First, it reads file 'movie_titles_canonical.txt' into a RDD and counts the number of lines; second, it connects to your neo4j database and creates a new node via bolt interface.

Let's make sure that you can run this program from your student VM. 

#### Deploy

1. Copy the program to your working directory (e.g. /home/ubuntu/workspace/SparkNeo4jSample.py).
2. Modify the initial variables in your favourite editor to match your environment (especially pay attention to NEO4J_PASS and PATH_TO_FILE entries).
3. Save the file.
4. Go to your home directory: `$ cd`
5. Submit the Spark job for local processing:
    ```shell
    $ spark-submit workspace/SparkNeo4jSample.py
    ```
#### Verify

1. The output log should contain following trace:
    ```log
    <trimmed>
    17/02/08 19:17:32 INFO TaskSchedulerImpl: Removed TaskSet 0.0, whose tasks have all completed, from pool
    17/02/08 19:17:32 INFO DAGScheduler: ResultStage 0 (count at /home/ubuntu/batch_cw/SparkStub.py:19) finished in 1.767 s
    17/02/08 19:17:32 INFO DAGScheduler: Job 0 finished: count at /home/ubuntu/batch_cw/SparkStub.py:19, took 1.887607 s
    ---
    
    
    Canonical movie count:  12862
    
    
    ---
    <trimmed>
    ```
2. Neo4j: Check that a node was created:

    ```
    MATCH (n:User {userId: 111}) RETURN n
    ```

### Cluster Deployment

Few things to note:

* Running a large cluster continuosly is an expensive endeavour, therefore a lot of effort (thanks Saleh!) was put into building an autoscaling Spark environment. The cluster will be available on request at first.
* Before contacting us, check if the cluster is running, by visiting [Spark master](http://52.213.206.26:8080) page. You should see a list of worker IDs under 'Workers' in ALIVE state.

![Spark Master - Workers](images/SparkMaster_workers.png)

* You need to make your Neo4j accessible via bolt interface from outside of your VM. Follow [these instructions](https://github.com/tomncooper/CSC8101-Documentation/blob/master/spark/python-stub/Neo4j-open-bolt-interface.md) to do so.

Ok so now you're ready!

#### Deploy

1. Follow 1-4 steps from Local Deployment section. Make sure that you change NEO4J_IP from 'localhost' to an IP address of your VM!
2. Run:

   ```shell
   $ spark-submit --master spark://ip-172-31-25-107.eu-west-1.compute.internal:7077 workspace/SparkNeo4jSample.py
   ```
   
#### Verify

Same as the Local Deployment.

**Well done! Any questions - let us know!**
