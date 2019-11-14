
DLRS template for OpenFaaS
==========================

Description
-----------

DLRS template for OpenFaaS deployments.

Usage
-----

.. code-block:: bash

   faas-cli new <project name> --lang python3-dlrs
   faas-cli up -f <project name>.yml

faas-cli up will build the image for the function, push it to the specified container registry and deploy the function to the running OpenFaaS instance. You are now ready to interact with the function.

Sample function
~~~~~~~~~~~~~~~

This function does nothing more than return the OS name.

.. code-block:: bash

   $ echo test | faas-cli invoke <project name> --gateway $<your gateway>

   NAME="Clear Linux OS"
   VERSION=1
   ID=clear-linux-os
   ID_LIKE=clear-linux-os
   VERSION_ID=30650
   PRETTY_NAME="Clear Linux OS"
   ANSI_COLOR="1;35"
   HOME_URL="https://clearlinux.org"
   SUPPORT_URL="https://clearlinux.org"
   BUG_REPORT_URL="mailto:dev@lists.clearlinux.org"
   PRIVACY_POLICY_URL="http://www.intel.com/privacy"
   0

Pix2Pix usecase using DLRS template for OpenFaaS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A machine learnig application using this template is available `here <https://github.com/intel/stacks-usecase/tree/master/pix2pix>`_.

License
-------

This project is licensed under the MIT license, see LICENSE file for further details.
