Installation
============

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
