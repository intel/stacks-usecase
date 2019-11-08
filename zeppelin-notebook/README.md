# DARS using Apache Zeppelin Notebook

Apache Zeppelin is a web-based notebook that enables interactive data analytics. With Zeppelin, you can make beautiful data-driven, interactive and collaborative documents with a rich set of pre-built language back-ends (or interpreters) such as Scala (with Apache Spark), Python (with Apache Spark), SparkSQL, Markdown, Angular, and Shell.

With a focus on Enterprise, Zeppelin has the following important features:

    Livy integration (REST interface for interacting with Spark)
    Security:
        Execute jobs as authenticated user
        Zeppelin authentication against LDAP
        Notebook authorization

The purpose of this tutorial is to explain  how to start Apache-Spark DARS plus Apache-Zeppelin, performing it either manually or using the scripts contained
in this repository to deploy it automatically and guide you through basic functionalities of Zeppelin so that you may create your own data analysis applications or import existent Zeppelin Notebooks.

***

## Software requirements

* Git
* JDK 1.8
* Maven
* Docker

***

## Automatic Setup and Initialize Process

There is a couple of scripts, Dockerfile and configuration files to setup and start for you Apache-Spark DARS plus Apache-Zeppelin notebooks.

The main tool is `stacks-zeppelin.sh`, this script is split in parts:

* Clone and build zeppelin.
* Copy configuration files to built cloned zeppelin folder. _(like interpreter presets, xml and env zeppelin files and few Notebooks)_.
* Build an image on top of DARS binding the cloned zeppelin folder and starting services and opening required ports.
* Start the container with the built image to access to Apache-Spark DARS plus Apache-Zeppelin.
* Stop the container built.

1. Execute the tool. _(Use  `-h` to get help)_. to build Apache-Zeppelin project. We use the latest one in master since this has support for Scala 2.12 required by DARS Apache Spark.

```bash
./stacks-zeppelin.sh -a build_zeppelin
```

2. Copy the required config files

```bash
./stacks-zeppelin.sh -a copy_files
```

3. Build Apache-Spark DARS plus Apache-Zeppelin

```bash
./stacks-zeppelin.sh -a build_image
```

4. Start Apache-Spark DARS plus Apache-Zeppelin

```bash
./stacks-zeppelin.sh -a start_zeppelin
```

5. Access to the Apache-Zeppelin Web UI YOUR-IP:8082

***

## Manual Setup and Initialize Process

Described below are the steps to:

* Build Apache-Zeppelin
* Initialize Apache-Spark plus Apache-Zeppelin
* Setup Apache-Zeppelin Interpreter

### Build Apache-Zeppelin

1. Clone Zeppelin repository:

```bash
git clone https://github.com/apache/zeppelin.git
```

2. Compile using maven and the flags indicated below to make it compatible with Spark + Scala  packaged in DARS:

```bash
cd zeppelin && mvn clean package -Pspark-2.4 -Pscala-2.12 -DskipTests
```

### Configure Apache-Zeppelin

1. In Apache-Zeppelin folder rename `conf/zeppelin-site.xml.template` and edit it as `conf/zeppelin-site.xml`

```bash
cp conf/zeppelin-site.xml.template conf/zeppelin-site.xml
```

2. Modify By default `zeppelin.server.addr` is `127.0.0.1`, change it if you will access to it from another machine or, as your needs.

   By default `zeppelin.server.port` is `8080`, but since Apache-Spark also uses this port, let's change these value.

Node `zeppelin.server.addr`:

```bash
<property>
  <name>zeppelin.server.addr</name>
  <value>YOUR-IP</value>
  <description>Server address</description>
</property>
```

Node `zeppelin.server.port`:

```bash
<property>
  <name>zeppelin.server.port</name>
  <value>8082</value>
  <description>Server port.</description>
</property>
```

3. In Apache-Zeppelin folder rename `conf/zeppelin-env.sh.template` and edit it as `conf/zeppelin-env.sh`

```bash
cp conf/zeppelin-env.sh.template conf/zeppelin-env.sh
```

4. Add at the end of `conf/zeppelin-env.sh` file the following line to change the file system to local:

```bash
export SPARK_SUBMIT_OPTIONS='--conf "spark.hadoop.fs.defaultFS=file:///" '
```

### Initialize DARS and Apache-Zeppelin

1. Run a container from DARS to be prepare to be linked with Apache-Zeppelin:

```bash
docker run -dit --cpus 2 -m 2G \
--ulimit nofile=1000000:1000000 -e SPARK_MASTER_PORT=7077 \
-p 4040:4040 -p 8080:8080 -p 7077:7077-p 8081:8081 -p 8082:8082 \
--mount type=bind,src=$(pwd)/zeppelin,dst=/opt/zeppelin \
 -h sparkmaster \
--name dars_standalone clearlinux/stacks-dars-mkl:v0.1.2
```

2. Start the Master and Slave daemons inside the container:

```bash
docker exec dars_standalone /usr/share/apache-spark/sbin/start-master.sh
docker exec dars_standalone bash -c "/usr/share/apache-spark/sbin/start-slave.sh spark://sparkmaster:7077"
```

3. Start Zeppelin Daemon

```bash
docker exec dars_standalone bash -c "/opt/zeppelin/bin/zeppelin-daemon.sh start"
```

>Note: If you want to use `IPython` you need to install it in DARS:
$ docker exec dars_standalone bash -c "pip install ipython"

>Note: To use `pyplot` or other matplotlib functions install them:
$ docker exec dars_standalone bash -c "pip install matplotlib"

>Note: To use `numpy` install it:
$ docker exec dars_standalone bash -c "pip install numpy"

>Note: To use `pandas` install it:
$ docker exec dars_standalone bash -c "pip install pandas"

### Setup Apache-Zeppelin Spark Interpreter

1. Access to the Apache-Zeppelin Web UI YOUR-IP:8082

2. Go to upper right corner, you should see an `anonymous` button. Click on it and select `Interpreter`

3. Search `spark` and click on `edit`

4. Configure as following:

| *name*   |                     *value*                    | *description*                                                               |
| ------------ | :--------------------------------------------: | :-------------------------------------------------------------------------- |
| master  | spark://sparkmaster:7077    | Use the DARS Spark container instance. |
| zeppelin.pyspark.useIPython  | false    | Disable the usage of Ipython, if you require to use it then leave it as it is and install ipython (See the notes above to see how to install it). |
| zeppelin.spark.useHiveContext   | false   | By default, zeppelin would use IPython in pyspark when IPython is available, Otherwise it would fall back to the original PySpark implementation. If you don't want to use IPython, then you can set as false. |

***

## Create a Notebook in Zeppelin

Now let's create your first notebook.
Creating a Notebook

To create a notebook:

1. Access to Zeppelin Web UI: YOUR-IP:8082

2. Click on `Notebook` and select `+ Create new note`

3. The previous will prompt you to a pop up window asking for a `Note Name` and a `Default Interpreter`. Select `spark` as interpreter and finally click on `Create`. 

By default the new notebook will be opened with a blank paragraph, if you want to come back to work on it at a later time you will find your notebook on the main Zeppelin UI.

4. Copy and paste the below code to process scala code by DARS container.

5. There are two ways of running a paragraph in a Zeppelin Notebook:

    * Click the play button (blue) triangle on the right hand side of the paragraph or

    * Press Shift + Enter

```bash
import scala.math.random

val slices = 100
val n = math.min(100000L * slices, Int.MaxValue).toInt
val xs = 1 until n
val rdd = sc.parallelize(xs, slices).setName("'Initial rdd'")
val sample = rdd.map { i =>
val x = random * 2 - 1
val y = random * 2 - 1
(x, y)
}.setName("'Random points sample'")

val inside = sample.filter { case (x, y) => (x * x + y * y < 1) }.setName("'Random points inside circle'")
val count = inside.count()
println("Pi is roughly " + 4.0 * count / n)
```

or

```bash
%pyspark
import random
NUM_SAMPLES = 1000000
def inside(p):
    x, y = random.random(), random.random()
    return x*x + y*y < 1

count = sc.parallelize(range(0, NUM_SAMPLES)).filter(inside).count()
print ("Pi is roughly %f" % (4.0 * count / NUM_SAMPLES))
```

More examples:

* Pyspark plotting:

```bash
%pyspark
import matplotlib.pyplot as plt
plt.plot([1, 6, 3])
plt.figure()
z.show(plt)
x = [0, 2, 4, 6, 8]
y = [0, 3, 3, 7, 0]
plt.plot(x, y)
z.show(plt)
```

***

## Import Notebooks in Zeppelin

Great, now you know how to create a notebook from scratch. Before we being coding, let's learn about different ways to import an already existent Zeppelin Notebook.
Importing a Notebook

Instead of creating a new notebook, you may want to import an existing one.

There are two ways to import Zeppelin notebooks, either by pointing to json notebook file local to your environment or by providing a url to raw file hosted elsewhere, e.g. on github. We'll cover both ways of importing those files.

1. Importing a JSON file

On the Zeppelin UI click Import.

`import-note`

Next, click Select JSON File button.

`import-from-json-zepp`

Finally, select the notebook you want to import and click Open.

`import-from-json-select-file`

Now you should see your imported notebook among other notebooks on the main Zeppelin screen.

2. Importing a Notebook with a URL

Click Import note.

`import-note`

Next, click Add from URL button.

`import-from-url-zepp`

Finally, paste the url to the (raw) json file and click on Import Note.

`import-from-url-zepp-paste`

Now you should see your imported notebook among other notebooks on the main Zeppelin screen.
Deleting a Notebook

If you would like to delete a notebook you can do so by going to the Zeppelin Welcome Page. On the left side of the page under Notebook you will see various options such as Import note, Create new note, a Filter box, right under the Filter box is where you will find notebooks that you created or imported.

To delete a notebook(see image below as reference)

1. Hover over the notebook that you want to delete

Various icons will appear including a trashcan.

2. Click on the trashcan icon

`deleting_a_notebook`

A prompt will ask you if you want to Move this note to trash?, click OK.

The notebook has now been moved to the Zeppelin's trash folder. You can always restore the notebook back by clicking on the Trash folder, hover over the notebook you want to restore, there you will see two options a curved arrow that says Restore note and an x that allows you to remove items permanently. If you want to restore an notebook click on Restore note and on x to delete the item permanently from Zeppelin.
Adding a Paragraph

By now you must be eager to begin coding or expanding on the notebook you imported. Adding a paragraph in Zeppelin is very simple. Begin by opening the notebook that you want to work on, for this part of the tutorial we will use the Spark On HDP Notebook we created earlier.

Next, hover over either the lower or upper edge of an existent paragraph and you will see the option to add a paragraph appear.

`add-paragraph-hover-above`

Click above to add the new paragraph before the existent one.

`add-paragraph-hover-below`

Or click below to add the new paragraph after the current paragraph.

Okay, now that you have either created or imported a notebook and wrote paragraphs, the next step is to run the paragraphs.
Running a Paragraph

To clear the output of a specific paragraph:

1. Click on the gear located on the far right hand side of the paragraph.

2. Select Clear Output

Clearing the Output of a Paragraph

This will clear the output of that specific paragraph

To clear the output of the whole Zeppelin Notebook go to the top of the Notebook and select the eraser icon. A prompt will appear asking Do you want to clear all output? Press OK.
