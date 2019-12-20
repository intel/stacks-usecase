# Stacks Usecase: Identify Galaxies Using the Deep Learning Reference Stack

### PREREQUISITES:
- Intel Xeon Processor with AVX512 enabled
- Familiarity with Docker
- Familiarity with git
- Familiarity with Python

### DATA RETRIEVAL 
In order to run this demo, it is needed to download de weights and labels to train the model first.
Downlad Table 2 CSV file from [Galaxy Zoo](https://data.galaxyzoo.org/) page. After downloading it is needed to work on the CSV file since it comes by
default with the galaxies celestial coordinates in degrees, and it will be necessary to convert to decimal units in order to download the images from the SDSS site.

### DATA PREPARATION
The CSV file downloaded from Galaxy Zoo, you will find in the head the following columns

| OBJID | RA | DEC | NVOTE | P_EL | P_CW | P_ACW | P_EDGE | P_DK | P_MG | P_CS | P_EL_DEBIASED | P_CS_DEBIASED | SPIRAL | ELLIPTICAL | UNCERTAIN | 
|-------|----|-----|-------|------|------|-------|--------|------|------|------|---------------|---------------|--------|------------|-----------| 

Where:

* OBJID = galaxy ID
* RA = Right Ascension
* DEC = Declination
* NVOTES = Number of votes for the galaxy/object

Fraction of votes for:

* P_EL = Elliptical category
* P_CW = Clockwise spiral
* P_ACW = Anticlockwise spiral
* P_EDGE = Ege-on
* P_DK = don't know
* P_MG = Merger
* P_CS = Combined spiral


Debiased votes:

* P_EL_DEBIASED = for elliptical
* P_CS_SPIRAL = for combined spiral categories


SPIRAL, ELLIPTICAL and UNCERTAIN are flags for galaxies with 80 percent of the vote after debiasing.

Delete the latest 3 columns from the CSV file
*  SPIRAL
*  ELLIPTICAL
*  UNCERTAIN
 
The resulting file must have the following columns

| OBJID | RA | DEC | NVOTE | P_EL | P_CW | P_ACW | P_EDGE | P_DK | P_MG | P_CS | P_EL_DEBIASED | P_CS_DEBIASED | 
|-------|----|-----|-------|------|------|-------|--------|------|------|------|---------------|---------------| 

In order to download the images from SDSS you have to convert the celestial coordinates from degrees to decimal units, this is helpful since the SDSS has a [bulk download tool](http://skyserver.sdss.org/dr7/en/tools/chart/list.asp), but in order to retrieve the data you need to the celestial coordinates in decimal units.

In the [SDSS DR7 Image List Tool](http://skyserver.sdss.org/dr7/en/tools/chart/list.asp) you can query up to 1000 objets with their right ascension and declination values in decimal units.



The easiest way to convert units and with high precision is using astropy library for Python, you will need to import a few modules from astropy 
and create a function like the next one:

```python
from astropy.coordinates import SkyCoord
from astropy import units as u

def convert_to_dec(ra, dec):
    dec_coord = SkyCoord(ra=ra, dec=dec, unit=(u.hourangle, u.deg))
    return dec_coord

```
Assuming you have preloaded your coordinates.

For example the conversion of OBJID 587727178986356823 

*  Original values of celestial coordinates in degrees

| OBJID              | RA          | DEC         | NVOTE | P_EL | P_CW  | P_ACW | P_EDGE | P_DK  | P_MG  | P_CS  | P_EL_DEBIASED | P_CS_DEBIASED | 
|--------------------|-------------|-------------|-------|------|-------|-------|--------|-------|-------|-------|---------------|---------------| 
| 587727178986356823 | 00:00:00.41 | -10:22:25.7 | 59    | 0.61 | 0.034 | 0.0   | 0.153  | 0.153 | 0.051 | 0.186 | 0.61          | 0.186         | 


*  Converted values of celestial coordinates in decimal units
  

| OBJID              | RA         | DEC          | NVOTE | P_EL | P_CW  | P_ACW | P_EDGE | P_DK  | P_MG  | P_CS  | P_EL_DEBIASED | P_CS_DEBIASED | 
|--------------------|------------|--------------|-------|------|-------|-------|--------|-------|-------|-------|---------------|---------------| 
| 587727178986356823 | 0.00170833 | -10.37380556 | 59    | 0.61 | 0.034 | 0.0   | 0.153  | 0.153 | 0.051 | 0.186 | 0.61          | 0.186         | 


You must download all the images you want to train and each image you download has to have as a filename the same value as it's corresponding OBJID value with jpg extension name.
For example the image corresponding to OBJID 587727178986356823, has to be named like this 587727178986356823.jpg

One way to download images is found [here](http://skyservice.pha.jhu.edu/DR7/ImgCutout/getjpeg.aspx?ra=0.05329166666666666&dec=1.1201944444444445&scale=0.40&width=480&height=480&opt=). You would need
to modify the right ascension and declination and image dimension values through scripting by replacing the RA and DEC variables in the the URL.

SDSS has other download methods as well, you can use any other method to retrieve the images, however is importart to rename the images to make them match to it's corresponding OBJID in the CSV file

The SDSS has more resources and tools to access the data in their web page, [SDSS DR7 Tools for data access](https://classic.sdss.org/dr7/access/)

Once you have all the images, we have to edit the CSV file one more time, to include only the data that is required for the training algorithm, we only need the following columns from our CSV file

| OBJ_ID | P_EL | P_CW | P_ACW | P_EDGE | P_DK | P_MG | P_CS | P_EL_DEBIASED | P_CS_DEBIASED | 
|--------|------|------|-------|--------|------|------|------|---------------|---------------| 


#### Setup data files

In the repo you'll find a file called **globals.py**

```python
# Training directories
current_path = "/home/new_dataset/"
dataset_filename ="dataset.csv"

training_path = current_path + "images/"
training_csv_path = current_path + dataset_filename
pt_model_name = "galaxy_recognition_model.pt"

```

You may edit the file or match your data to be named and placed in the directories listed there

For example, the training directories are by default configured to be in ***/home/new_dataset/*** 
And the dataset file name is expected to be named as ***dataset.csv***

The same goes for the images, the images directory is configured by default to be in ***/home/new_dataset/images*** 

The pytorch trained model will be saved by default as ***galaxy_recognition_model.pt***



### GALAXY RECOGNITION
1. Pull the DLRS image to the local machine
```shell
docker pull clearlinux/stacks-pytorch-mkl
```

2. Run the container

```shell
docker run --ipc=host -id --name <container_name> stacks-pytorch-mkl /bin/bash
```

The `--ipc=host` flag should handle some errors regarding *shared memory* such as

`ERROR: Unexpected bus error encountered in worker. This might be caused by insufficient shared memory (shm).`

You could also replace it with `--shm-size` in the command line options

3. Install prerequisites inside the container:

First, clone the repo whit the Galaxy Recognition usecase code

```shell
git clone <galaxy_recognitio_repo>
```

In this part it is required to have the images saved inside the container and also a csv file with the weights to train the model. These data is free and available in the SDSS site.

You may also need to install the following python packages

```shell
pip install numpy pandas pillow scikit-image
```
Note: If you are using a different container or running in your host and you don't have Pytorch installed, you may create a virtual environment and install torch and torchvision:

```shell
mkdir <your_environment_name>
python -m venv <your_environment_name>
source <your_environment_name>/bin/activate
pip install numpy pandas pillow scikit-image torch torchvision
```

4. Train the model
```shell
python training.py
```

After running this script, the model should be created with *.pt extension, you need this model in order to run the inference.
Once you have the model, you don't need to run steps from 1 to 4, you can directly run the inference with the trained model as many times you want.

5. Run inference with trained model
```shell
python inference.py <id> <image.jpg>
```
Where parameters <id> can be an integer number to reference the result in an output csv file and <image.jpg> is the image of your choice to infer, must be in jpg format.
Following these steps, you will have a trained model capable of recognizing galaxies with the Deep Learning Reference Stack.



### OUTPUT DATA

The output data is a CSV file, similar to the Galaxy Zoo table used to train the model, all of the columns 


* Elliptical galaxy
* Clockwise Spiral galaxy
* Anticlockwise Spiral galaxy
* Edge-on (other) galaxy
* Star, Don’t Know
* Merger
* Combined Spiral Category
* Debiased Elliptical galaxy
* Debiased Spiral galaxy

### INTERPRETATION OF THE RESULTS

The resulting trained model should always be thought keeping in mind that the Galaxy Zoo results are the perception
of people and how they classify objects. In other words, the model built will be no other thing than an emulation of how 
people would vote if they were asked to classify a given image and thus, the values in each collumn represent the probabilites 
of a galaxy to belong to the given categories; the higher the value in one of the categories, more likely the chance is that if real
people were asked to vote on the object, they would classify it as of that category.


### REREFENCES

* https://clearlinux.org/stacks/deep-learning
* http://classic.sdss.org/
* http://classic.sdss.org/dr7/
* https://data.galaxyzoo.org/
* https://www.zooniverse.org/projects/zookeeper/galaxy-zoo/
* https://ui.adsabs.harvard.edu/abs/2008MNRAS.389.1179L/abstract
* https://ui.adsabs.harvard.edu/abs/2011MNRAS.410..166L/abstract
* https://arxiv.org/pdf/1605.07678.pdf


