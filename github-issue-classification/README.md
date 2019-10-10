# Github Issue Classification Usecase

### Introduction

Github issues are currently manually classified, but why not automate the tagging process? A simple ML algorithm can be used to analyze the issue content and tag it automatically, saving time for developers and directing their focus to critical issues. This usecase shows the user how to do exactly that.

To run the usecase locally, follow the steps below. You will need to manually preprocess the data using [DARS](https://hub.docker.com/r/clearlinux/stacks-dars-mkl) container which is an optimized spark container, train the data with [DLRS](https://hub.docker.com/r/clearlinux/stacks-dars-mkl) which is a deep learning container, then serve it with rest.py, and run the frontend within the website folder.

If you would prefer a simple walkthrough with a jupyter notebook, feel free to explore github-notebook.ipynb. It is a self contained and simplified example of this usecase. Instructions to use are located below under "Training the Model using DLRS and Jupyter Notebooks"


### Installation

To install and use the Data Analytics Reference Stack (DARS), refer [here](https://docs.01.org/clearlinux/latest/guides/stacks/dars.html)

To install and use the Deep Learning Refence Stack (DLRS), refer [here](https://docs.01.org/clearlinux/latest/tutorials/dlrs.html)


## Table of contents

* data
	* Where the raw and clean data is stored
* kubeflow
	* All cloud uses and implementations are here
* models
	* Where Machine Learning and vectorizer models are stored
* scripts
	* A bash script to retrieve data, and a scala script to process the data
* website
	* A flask based server that displays a front end on
	host to interact with the model
* Dockerfile
	* Builds an image based on DLRS that will automatically run rest.py
* Makefile
	* `make` command instructions for `Dockerfile`
* config.make
	* Configurations for the `Makefile`
* github-notebook.ipynb
	* A user friendly walkthrough and explanation of what's happening in `train.py`
* requirements.txt
	* Requirements needed in the DLRS image during inference
* rest.py
	* This file runs a RESTful API server that receives issue content and returns labels
* train.py
	* This file trains the model



## Local Container Walkthrough

Clone this repo and pull the DARS container:

```bash
git clone https://github.com/intel/stacks-usecase
```
```bash
docker pull clearlinux/stacks-dars-mkl:latest
```
```bash
cd stacks-usecase/github-issue-classification
```
```bash
docker run -it --ulimit nofile=1000000:1000000 -v ${PWD}:/workdir clearlinux/stacks-dars-mkl bash
```

#### Prepare the spark environment
In this section we will prepare our Spark environment using DARS.

First, create the output directory if it doesn't exist
```bash
cd /workdir
mkdir /data
mkdir /data/raw
```

Change the "get-data.sh" script to an executable and execute it to retrieve clearlinux issues data
```bash
cd /workdir/scripts
chmod u+x get-data.sh
./get-data.sh
cd /workdir
```
Note that you must be in the /workdir directory before starting Spark.

Run the spark shell
```bash
spark-shell
```

#### Process the data

1. Import session and instantiate a spark context

```bash
import org.apache.spark.sql.SparkSession
val spark = SparkSession.builder.appName("github-issue-classification").getOrCreate()
import spark.implicits._
```
2. Load the data to a spark dataframe
```bash
var df = spark.read.option("multiline", true).json("data/raw/*.json")
```
3. Select the labels, name, body, and id columns
```bash
df = df.select(col("body"), col("id"), col("labels.name"))
```
4. Explode the labels column to prepare for filtering the top labels
```bash
var df2 = df.select(col("id"),explode(col("name")).as("labels"))
```
5. Order the Labels by frequency
```bash
var df3 = df2.select("labels").groupBy("labels").count().orderBy(col("count").desc).limit(10).select("labels")
```
6. Turn the top labels into a list (to put into the next step)
```bash
var list = df3.select("labels").map(r => r.getString(0)).collect.toList
```
7. Filter the top labels
```bash
df2 = df2.filter($"labels".isin(list:_*))
```
8. Recombine the top labels
```bash
df2 = df2.groupBy("id").agg(collect_set("labels").alias("labels"))
```
9. Take intersection of label ids and body ids to get final list
```bash
df = df.join(df2, "id").select("body","labels")
```
10. Save the data
```bash
df.write.json("data/tidy/")
```
Or, from within the spark shell run:
```bash
:load -v scripts/proc-data.scala
```
The proc-data.scala script performs all the steps 2-10 described above.




#### Train a model using DLRS
In this section we will train a model using DLRS in preparation for serving it.

1. If you have not done so already, clone the usecases repo into your local workspace
```bash
git clone https://github.com/intel/stacks-usecase
```
```bash
cd stacks-usecase/github-issue-classification
```
2. Pull and run the Deep Learning Reference Stack (DLRS)
```bash
docker pull clearlinux/stacks-dlrs-mkl
```
```bash
docker run -it -v ${PWD}:/workdir clearlinux/stacks-dlrs-mkl
```
3. Navigate to the github usecase and install requirements
```bash
cd /workdir/docker
```
```bash
pip install -r requirements_train.txt
```
4. Create the output directory
```bash
mkdir /workdir/models
```
5. Run the training script
```bash
cd /workdir/python
```
```bash
python train.py
```

That's it! At its core, DLRS does not require that you change your code. Once the environment is set up (steps 1-4), a single call to your code will run as expected, and it will utilize Intel optimizations. This is the base functionality of DLRS, and most implementations will be built off this example section.


#### Serve the model
To run inference, we've set up a special dockerfile based on our image. The dockerfile creates a RESTful API that will communicate to a local flask server to run live inference.

From your local system, navigate to the github-issues-classification folder, where "Dockerfile" is stored inside the "docker" directory, and run:
```bash
make
```
```bash
docker run -p 5059:5059 -it github_issue_classifier:latest
```

It may seem like nothing happened, but with a few commands a REST API has been created running out of a docker container.

Now run one last step in a second terminal:
```bash
cd ../website
flask run
```
This will create a flask server on your local system. Open your favorite browser and navigate to localhost:5000 to see an interactive example of the guthub issues usecase. Simply copy or type any issue into the top left box, and hit submit. The flask server will call the REST API, which will process your input and return the appropriate labels.



## Training the Model using DLRS and Jupyter Notebooks

1. Pull and run the Deep Learning Reference Stack (DLRS). You will need to mount it to disk and connect a jupyter notebook port.
```bash
docker pull clearlinux/stacks-dlrs-mkl
docker run -it -v ${PWD}:/workdir -p 8888:8888 clearlinux/stacks-dlrs-mkl
```

2. From within the container, navigate to the workspace, install sklearn, and start a jupyter notebook that is linked to the exterior port. Make sure to copy the token from the output.
```bash
cd ../workdir
pip install sklearn
jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
```

3. Open a browser and navigate to localhost:8888. If the notebook asks for a token, paste the token from the previous step and submit. You now have a notebook running out of DLRS that can access any local files. We have a jupyter notebook prebuilt for you.


**NOTE**: If you get a 'hit rate limits' error when fetching raw json file from github API, you have to add the `-u "<github username>"` option to curl

## Mailing List

See our public [mailing list](https://lists.01.org/mailman/listinfo/stacks) page for details on how to contact us. You should only subscribe to the Stacks mailing lists using an email address that you don't mind being public.

## Reporting Security Issues

Security issues can be reported to Intel's security incident response team via https://intel.com/security.
