# Open Neo4j bolt interface 

To be polished...

on the VM 

1. Go the the file:
    ```
    $ sudo vim /etc/neo4j/neo4j.conf
    ```

2. Find line:
    ```
    # dbms.connector.bolt.address=0.0.0.0:7687
    ```

3. Uncomment:
    ```
    dbms.connector.bolt.address=0.0.0.0:7687
    ```

4. Save

5. Restart Neo4j

    ```shell
    $ sudo service neo4j restart
    ```
