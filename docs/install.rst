Installation Guide
==================

To install ``tk-facebook``, run the following commands in your terminal. It is **highly** reccomended that you initialize a virtual environment with ``virtualenvwrapper``:

.. code-block:: bash

   $ mkvirtualenv tk-facebook
   $ git clone https://github.com/newslynx/tk-facebook.git
   $ cd tk-facebook
   $ pip install -r requirements.txt
   $ pip install .

Tests can be run with ``nose`` in the projects root directory:

.. code-block:: bash

   $ nosetests


