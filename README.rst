Resoluciones UNC
================

Document processing, browsing and searching tool.


Installation
------------

1. Be sure you have the following software:

   - Git
   - Python 2.7
   - Pip
   - MongoDB 2.2 or newer

   In a Debian based system you can simply do::

    sudo apt-get install git python2.7 python-pip mongodb

2. Create and activate a new
   `virtualenv <http://virtualenv.readthedocs.org/en/latest/virtualenv.html>`_
   (or don't do it and let the dependencies be installed straight into your
   system).
   I recommend using `virtualenvwrapper
   <http://virtualenvwrapper.readthedocs.org/en/latest/install.html#basic-installation>`_.
   Install it with::

    pip install virtualenvwrapper

   Then add the following line at the end of your ``.bashrc``::

    [[ -s "/usr/local/bin/virtualenvwrapper.sh" ]] && source "/usr/local/bin/virtualenvwrapper.sh"

   and finally create and activate the virtualenv with::

    mkvirtualenv resoluciones-unc

   (may need ``--python=/usr/bin/python2.7`` if 2.7 is not the default version).

3. Download the code::

    git clone https://github.com/HackatONG-ProgramAR/resoluciones-unc

4. Install "Resoluciones UNC" and its dependencies::

    cd resoluciones-unc
    pip install -e .
    pip install -r requirements-all.txt

   (probably you will have to do ``sudo pip install .`` instead if you don't
   have a virtualenv).


Usage: Document Processing
--------------------------

1. First, activate your virtual environment. If you use ``virtualenvwrapper``::

    workon resoluciones-unc

2. Create the Mongo database::

    python process/scripts/createdb.py <dbname> <documents_path>

4. Process the documents::

    python process/scripts/run.py <dbname>


Usage: Document Browsing and Searching
--------------------------------------

We provide a `Django <https://www.djangoproject.com/>`_ web application to
browse the documents and the extracted information.
We also provide a search engine using
`Haystack <http://django-haystack.readthedocs.org>`_ and
`Whoosh <http://whoosh.readthedocs.org>`_.

1. As always, activate your environment. With ``virtualenvwrapper``::

    workon resoluciones-unc

2. Create the database and import the data::

    cd webapp
    python manage.py syncdb
    python manage.py mongoimport <dbname>

3. Index the data for the search engine::

    python manage.py rebuild_index

4. Run and open the web application::

    python manage.py runserver

   Visit http://127.0.0.1:8000/admin and http://127.0.0.1:8000/search.
