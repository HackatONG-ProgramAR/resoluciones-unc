"""
Database creation script.

Usage:
    createdb.py <dbname>
    createdb.py -h | --help | --version

Options:
  -h --help             Show this screen
  --version             Version number
"""
import logging
import os
import codecs
from docopt import docopt

from iepy.db import connect, DocumentManager


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('createdb')
    opts = docopt(__doc__, version=0.1)
    dbname = opts['<dbname>']

    connect(dbname)
    docs = DocumentManager()

    # Create the documents.
    for i in [7, 30, 102]:
        filename = 'RHCD_{}_2014.txt'.format(i)
        file_path = os.path.join('data', 'examples', filename)
        file_text = codecs.open(file_path, encoding='utf-8').read()

        docs.create_document(
            identifier=filename, # a unique identifier
            text=file_text,
            metadata={
                # anything you want here
                'number': i,
                'year': 2014,
                'files': [(file_path, '', 0)],
            })

    logger.info('Created database %s', dbname)
