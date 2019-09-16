import org.apache.spark.sql.SparkSession
val spark = SparkSession.builder.appName("github-issue-preprocess").getOrCreate()
import spark.implicits._

var dataset = "/workdir/data/raw/"
if(sys.env.getOrElse("DATASET_NAME", "/workdir/data/raw/") != "/workdir/data/raw/") {
        dataset = "/opt/dkube/dataset/" + sys.env.get("DATASET_NAME").get
}
dataset = dataset + "/*.json"

var outdir = sys.env.getOrElse("OUT_DIR","/workdir/data") + "/tidy"

var df = spark.read.option("multiline", true).json(dataset)
df = df.select(col("body"), col("id"), col("labels.name"))
var df2 = df.select(col("id"),explode(col("name")).as("labels"))
var df3 = df2.select("labels").groupBy("labels").count().orderBy(col("count").desc).limit(10).select("labels")
var list = df3.select("labels").map(r => r.getString(0)).collect.toList
df2 = df2.filter($"labels".isin(list:_*))
df2 = df2.groupBy("id").agg(collect_set("labels").alias("labels"))
df = df.join(df2, "id").select("body","labels")
df.write.json(outdir)
System.exit(0)
