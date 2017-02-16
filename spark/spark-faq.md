# Spark Coursework - Frequently Asked Questions

Please make sure you have consulted the 
[Spark Documention](http://spark.apache.org/docs/latest/), the
[programming guide](http://spark.apache.org/docs/latest/programming-guide.html)
and the API documentation for your chosen language:

- [Python](http://spark.apache.org/docs/latest/api/python/index.html)
- [Java](http://spark.apache.org/docs/latest/api/java/index.html)
- [Scala](http://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.package)

Also make sure you have read the instructions in the 
[coursework specification](spark-coursework-spec.md).

# FAQ content

* [Neo4j](https://github.com/tomncooper/CSC8101-Documentation/blob/master/spark/spark-faq.md#neo4j)
* [Running Spark](#runningspark)
* [Spark in general](#sparkingeneral)

## Neo4j

### I cannot access neo4J from my Jupyter Notebook!

You may need to run the following command on your VM:

`$ sudo pip3 install neo4j-driver`

This should insure that the Python 3 neo4j driver is properly installed.

### I cannot access neo4j web interface on port 7474 (404 Error).

Your neo4j database is most likely down. Login to your VM and run:

`$ sudo neo4j start`

Try to load the webpage again.

## Running Spark

### How many Spark worker threads are running on my iPython notebook?

You can check the number of threads by running following command directly in your iPython notebook:

`print("Number of worker threads:", sc.getConf().get("spark.master"))`
    
Check the result against the table in the [documentation](http://spark.apache.org/docs/latest/submitting-applications.html#master-urls).  

By default SparkContext will run with as many worker threads as logical cores on your machine.

### How can I modify Spark resources available to my iPython notebook?

When starting your iPython notebook from the shell command line on your student VM, you can specify specific resource allocation (e.g. number of executors, driver RAM memory, executor RAM memory, etc):

`$ pyspark --num-executors 5 --driver-memory 2g --executor-memory 2g`

### Do I have to use Jupyter Notebooks to write my python code?

No you don't!

If you would prefer to enter commands directly into a command line interpreter
(REPL) then run the following command on your VM:

`$ ~/scripts/ipyspark.sh` 

This will change the config setting of pyspark and launch it in a command line
interpreter. After running this command calling the `pyspark` command will 
always launch a command line interpreter. After a reboot the default notbook 
config will be reinstated so you will have to run the ipyspark script again.

Be aware that commands entered into the command line interpreter are not saved
and will be lost when you close the interpreter (Ctrl+D). The command line 
interpreter is best used for testing commands. You should write your Python code
in a text editor (`nano` or `vim` are available on the VMs) and save it to a 
`.py` file. You can use the following command to test you code file locally on 
your VM:

`$ spark-submit --master "local[2]" my_python_file.py`

If you have called `ipyspark` but wish to go back to the notebook version 
without rebooting use the command below:

`$ ~/scripts/pyspark-notebook.sh`

This will change the configs back to their defaults and launch the notebook 
server.

### How do I reduce spark console output?

By default Spark will output a lot of information about its internal working
when you run a local job.

If you don't want to see this during development on your local machine you 
can change the logging level by using the process below:

From your home directory run the following command: 

`$ cp spark/conf/log4j.properties.template spark/conf/log4j.properties`

This will create a new logging config file. You then need to edit this file
using whatever console based text editor you are happy with, `nano` or `vim` are
pre-installed on your VMs. 

`$ nano spark/conf/log4j.properties` 

You the need to change the following line from this:

`log4j.rootCategory=INFO, console`

To this:

`log4j.rootCategory=ERROR, console`

Once you save this file, the next time you run spark you will only see errors
and any print or rdd.pprint command outputs.

## Spark in general

### My program is taking a long time to execute

Within reason, this is to be expected. If you remember the lecture on the subject,
you will remember that the [ALS](http://spark.apache.org/docs/latest/mllib-collaborative-filtering.html)
algorithm is iteratively trying to adjust all the values of two latent factor matrices
(containing roughly 2.5M elements) so that specific values in their dot product
closely match all of the 95M known ratings. Even just considering the integer
operations, your VMs **cannot do this in 2 minutes of running time**, as you may
be used to from previous assignments. This is _Big_ Data after all.

Exactly how long your program runs depends on many factors. Most importantly how
you have written it, but also other less important things such as the programming
language you have chosen to use (Ahem ... see **Sidenote on Python**).

Depending on the particulars of your solution, you can expect running times anywhere
from around **10 minutes** up to around **40 minutes**. Any longer than this and
there is probably something wrong. That may seem like a wide range, but think of
it in terms of a program which will run for 5 seconds or 20 seconds.

If your program is running slowly, or failing after a long time and making debugging
tedious then there are things you can do:

--------------------------

1. Try calling `.persist()` (and perhaps `.unpersist()`) on your `RDD`s. `RDD`s are lazily
evaluated which means that when you chain several operations (`map`, `filter` and
friends) on one, nothing happens right away. However if you then do something which
forces an `RDD` to be materialised (e.g. pass it to `ALS.train`, or call `collect`,
`join` etc...) then all those chained operations are evaluated for each `RDD`
element. For reasons of saving memory, the results of these operations are not
kept around by default. This means that if you materialise an `RDD` multiple times
all those earlier operations are repeated. The solution to this problem is the
`persist` operation, which is explained [here](http://spark.apache.org/docs/latest/programming-guide.html#rdd-persistence).

2. Make sure you are using the right methods on `ALS`. The training is likely to
be the most expensive part of your program. You need to make sure you are using
the **RDD-based API** (as instructed in the docs). The model training part of
your program should look similar to the code sampes on [this](http://spark.apache.org/docs/latest/mllib-collaborative-filtering.html)
page. Specifically, make sure you are calling the `ALS.train` method. If you
are calling `ALS.fit` **you are using the wrong API**.

3. Use a subset of the ratings file found [here](https://s3-eu-west-1.amazonaws.com/csc8101-spark-assignment-data/mv_all_1000_simple.txt). This is hitting your performance
problems with a metaphorical hammer :) , but it will likely work as the file above only
contains 1/20th the number of ratings. Be aware that the model produced will not
predict sensible ratings, but will allow you to progress with the coursework (after
all, none of the steps after model training _technically_ require that the model be
accurate), which is more important.

4. Try different tuning parameters. During the lecture on the workings of the
ALS algorithm (delivered by Hugo Firth) you were told what the parameters
(_rank_, _iterations_ etc...) meant. From this you should be able to extrapolate
the effect of changing them. Be aware that reducing the rank of latent factor
matrices and the number of iterations performed will reduce the predictive
accuracy of your model. 3 would be an absolute minimum for both.

--------------------------

If you are suffering performance issues you should attempt the first two steps above.
Failing this, you should seek the advice of a demonstrator, either in session or via a [github issue](https://github.com/tomncooper/CSC8101-Documentation/issues).

However if you continue to be stuck, then please try one or both of the last steps.
You will lose some marks for having a less accurate model, but far fewer than if you
do not attempt any of the subsequent tasks in the coursework.

### Sidenote on Python

I like to think of the way Python sends instructions to your CPU as not disimilar
to the way the fellowship took the one ring to mount Doom. [Slowly](http://benchmarksgame.alioth.debian.org/u64q/python.html).

Just occasionally the fellowship (Python) will do what you expect and get on the
back of an eagle (execute some C) to speed things up. Unfortunately they rarely
do this **when** you expect (on the way back?!) and eagles (C programs) have problems
of their own, namely: they have big beaks and claws and if they drop you
you might just fall into an active volcano.

Fortunately, like destroying the ring, spark batch jobs usually only need running
once; you can go ahead and entrust the "fate of the world" to digital hobbits
if you like... :)

**Disclaimer**: relax, the creators of pyspark are pretty smart. Its actually C or Java a lot of the time under the hood and the overhead is [likely very small](http://stackoverflow.com/questions/30477982/python-vs-scala-for-spark-jobs). [Here](https://cwiki.apache.org/confluence/display/SPARK/PySpark+Internals) is a link for the curious on how Pyspark works.
