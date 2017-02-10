# Cassandra Coursework - Frequently Asked Questions

Please make sure you have consulted the 
[Cassandra Documention](http://cassandra.apache.org/doc/latest/) and the API
documentation for your chosen language:

- [Python](http://datastax.github.io/python-driver/index.html)
- [Java](http://docs.datastax.com/en/developer/java-driver/3.1/)
- [Scala](https://github.com/outworkers/phantom)

Also make sure you have read the instructions in the 
[coursework specification](cassandra-coursework-spec.md).

## How do I access cassandra from my Jupyter notebook?

In order for your Python notebook to talk to Cassandra you need install the 
Python 3 version of the driver. On your vm run the following command:

`$ pip3 install cassandra-driver --user`

The install process may take some time, so be patient.
