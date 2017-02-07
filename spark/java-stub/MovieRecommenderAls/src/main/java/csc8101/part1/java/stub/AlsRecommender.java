package csc8101.part1.java.stub;

import java.util.Arrays;
import java.util.List;

import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.api.java.function.Function;
import org.apache.spark.api.java.function.PairFunction;
import org.apache.spark.api.java.function.VoidFunction;
import org.apache.spark.mllib.recommendation.ALS;
import org.apache.spark.mllib.recommendation.MatrixFactorizationModel;
import org.apache.spark.mllib.recommendation.Rating;
import org.neo4j.driver.v1.Session;

import scala.Tuple2;
import scala.Tuple3;

public class AlsRecommender {

	public static void main(String[] args) {
		
		// Turn off unnecessary logging
		Logger.getLogger("org").setLevel(Level.OFF);
		Logger.getLogger("akka").setLevel(Level.OFF);
		Logger log = Logger.getRootLogger();
		log.setLevel(Level.WARN);
		log.setAdditivity(false);
		
		// Create Java spark context
		SparkConf conf = new SparkConf().setAppName("Collaborative Filtering Example").setMaster("local[2]");
		JavaSparkContext sc = new JavaSparkContext(conf);
		
		// Continue .............
		JavaRDD<String> printTest = sc.parallelize(Arrays.asList(new String[]{"From", "here", "on", "add", "your", "own", "code"}));
		printTest.foreach(new VoidFunction() {
			@Override
			public void call(Object string) throws Exception {
				System.out.println(string);			
			}			
		});		
	}
}