import org.apache.spark.sql.SparkSession
val spark = SparkSession.builder.appName("github-issue-preprocess").getOrCreate()
import spark.implicits._

var df = spark.read.option("multiline", true).json("/workdir/data/raw/*.json")
df = df.select(col("body"), col("id"), col("labels.name"))
var df2 = df.select(col("id"),explode(col("name")).as("labels"))
var df3 = df2.select("labels").groupBy("labels").count().orderBy(col("count").desc).limit(10).select("labels")
var list = df3.select("labels").map(r => r.getString(0)).collect.toList
df2 = df2.filter($"labels".isin(list:_*))
df2 = df2.groupBy("id").agg(collect_set("labels").alias("labels"))
df = df.join(df2, "id").select("body","labels")
df.write.json("/workdir/data/tidy")
System.exit(0)
