from pyspark import SparkContext, SparkConf
from neo4j.v1 import GraphDatabase, basic_auth

APP_NAME = "Batch coursework"
MASTER = "local"
NEO4J_IP = "localhost"
NEO4J_USER = "neo4j"
NEO4J_PASS = "supersecret"

PATH_TO_FILE = "data/movie_titles_canonical.txt"

if __name__ == "__main__":
    # get a spark context
    conf = SparkConf().setAppName(APP_NAME).setMaster(MASTER)
    sc = SparkContext(conf=conf)

    # load a text file
    can_movies = sc.textFile(PATH_TO_FILE).cache()
    can_movies_count = can_movies.count()

    # make some space and print line count
    print("%s%s%s"% ("\n"*2, "---", "\n"*2))
    print("Canonical movie count: ", can_movies_count)
    print("%s%s%s"% ("\n"*2, "---", "\n"*2))

    # write to neo4j db
    user_id = 111
    user_motto = "live long and prosper"
    driver = GraphDatabase.driver("bolt://%s:7687" % NEO4J_IP, auth=basic_auth(NEO4J_USER, NEO4J_PASS))
    session = driver.session()
    session.run("CREATE (a:User {userId: {userId}, motto: {motto}})", {"userId": user_id, "motto": user_motto})
    session.close()
