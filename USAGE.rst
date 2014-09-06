Usage
=====

Document Processing
-------------------

1. First, activate your virtual environment. If you use ``virtualenvwrapper``::

    workon resoluciones-unc

2. Create the Mongo database::

    python process/scripts/createdb.py <dbname> <documents_path>

4. Process the documents::

    python process/scripts/run.py <dbname>


Document Browsing and Searching
-------------------------------

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
