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

### I cannot access neo4J from my Jupyter Notebook!

You may need to run the following command on your VM:

`$ sudo pip3 install neo4j-driver`

This should insure that the Python 3 neo4j driver is properly installed.

### I cannot access neo4j web interface on port 7474 (404 Error).

Your neo4j database is most likely down. Login to your VM and run:

`$ sudo neo4j start`

Try to load the webpage again.

### How many Spark worker threads are running on my iPython notebook?

You can check the number of threads by running following command directly in your iPython notebook:

`print("Number of worker threads:", sc.getConf().get("spark.master"))`
    
Check the result against the table in the [documentation](http://spark.apache.org/docs/latest/submitting-applications.html#master-urls).   

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
