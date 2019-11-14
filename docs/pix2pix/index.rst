.. role:: raw-html-m2r(raw)
   :format: html


PIX 2 PIX
=========

Artists are faced with the challenge of effectively synthesizing photos from label maps, reconstructing objects from edge maps or colorizing images, among other tasks. Pix2pix is a fun, popular cGAN deep learning model that, given an abstract input, can create artistic outputs. 

.. raw:: html

   <pre>
       Generated image                     Target image             Input image
   </pre>




.. image:: ./images/example.jpg
   :target: ./images/example.jpg
   :alt: output_target_input



The code has been developed in such a way that, any new dataset can be easily added and the cGAN trained with it. We are also opensourcing a web front-end, components to deploy pix2pix inference as a function as service with openfaas as well. The pix2pix architecture is complex, but utilizing it is easy and an excellent showcase of the abilities of the Deep Learning Reference Stack. 

Instructions
^^^^^^^^^^^^

Set up

.. code-block::



   #. If you have not done so already, clone the usecases repo into your local workspace
      .. code-block:: bash

         git clone https://github.com/intel/stacks-usecase

      .. code-block:: bash

         cd usecases/tensorflow/pix2pix

   #. Create the ``pix2pix-train`` docker image that utilizes DLRS

   .. code-block:: bash

      make train


   #. Instantiate the image

   .. code-block:: bash

      make run-trainer


   #. Download the data and process it
      .. code-block:: bash

         python scripts/get_data.py

      .. code-block:: bash

         python scripts/split.py

   Training
   ~~

Run training

.. code-block:: bash

   python main.py


If you want to adjust hyperparamaters like cycles, epochs, and batche_size, or even train the discriminator or generator separately, add them as arguments. For example:

.. code-block:: bash

   python main.py
   or
   python main.py --model continue --size_batch 12 --cycles 200


Available options are:


* 
  model (string)


  * continue - run models named 'generator_model.h5' and 'discriminator_model.h5' in the 'models' directory
  * checkpoint - run the latest model in the 'checkpoints' directory

* 
  cycles (int)

* size_batch (int)
* check_freq (int)

For more information on what each option does, run:

.. code-block:: bash

   python main.py --help


Inference
:raw-html-m2r:`<del>~</del>`\ ~~~~

.. code-block:: bash

   python infer.py <path to your image>


Testing
^^^^^^^


* Move to pix2pix directory 
* Install test requirements using:

.. code-block:: bash

   pip install -r test-requirements.txt




* Run 

.. code-block:: bash

   python -m pytest


Citation
--------

The original pix2pix paper:

.. code-block::

   @article{pix2pix2017,
     title={Image-to-Image Translation with Conditional Adversarial Networks},
     author={Isola, Phillip and Zhu, Jun-Yan and Zhou, Tinghui and Efros, Alexei A},
     journal={CVPR},
     year={2017}
   }


The owner of the facades dataset:

.. code-block::

   @INPROCEEDINGS{Tylecek13,
     author = {Radim Tyle{\v c}ek and Radim {\v S}{\' a}ra},
     title = {Spatial Pattern Templates for Recognition of Objects with Regular Structure},
     booktitle = {Proc. GCPR},
     year = {2013},
     address = {Saarbrucken, Germany},
   }
