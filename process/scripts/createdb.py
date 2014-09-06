"""
Database creation script.

Usage:
    createdb.py <dbname> <documents_path>
    createdb.py -h | --help | --version

Options:
  -h --help             Show this screen
  --version             Version number
"""
import logging
from docopt import docopt

from iepy.db import connect, DocumentManager


def create_document(document):
    doc = docs.create_document(
            identifier=document['metadata']['number'],
            text=document['text'],
            metadata=document['metadata'])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('createdb')
    opts = docopt(__doc__, version=0.1)
    dbname = opts['<dbname>']
    documents_path = opts['<documents_path>']

    connect(dbname)
    docs = DocumentManager()

    # Create the documents.
    for i in range(10):
        docs.create_document(
            identifier='document{0:02}'.format(i), # a unique identifier
            text='', # plain text of the document. you can leave this empty
                     # and fill it in the first step of the preprocessing.
            metadata={
                # anything you want here
                'raw_data': 'Raw content of document {0}.'.format(i),
                'number': i,
                'files': [('{}.txt'.format(i), '', 0)],
            })

    logger.info('Created database %s', dbname)
